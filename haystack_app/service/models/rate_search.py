from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import BM25Retriever, DensePassageRetriever
from haystack.pipelines import DocumentSearchPipeline
from haystack.utils import convert_files_to_docs, fetch_archive_from_http


def con_elastic(host, index):
    return ElasticsearchDocumentStore(
        host=host,
        username="",
        password="",
        index=index,
    )


# elastic search 호스트 이름 정의 / local: "localhost", docker: "elasticsearch_for_haystack_app"
ELASTIC_HOST_NAME = "elasticsearch_for_haystack_app"

# 판례 sbert
document_store_rate_sb = con_elastic(ELASTIC_HOST_NAME, "rate_sb")
# 판례 bm25
document_store_rate_bm = con_elastic(ELASTIC_HOST_NAME, "rate_bm")


# s3에서 데이터 저장
doc_dir = "rate_data"
s3_url = "https://d2x9t9mzd36q83.cloudfront.net/fault_rate/fault_rate_1.zip"
fetch_archive_from_http(url=s3_url, output_dir=doc_dir)


# 파일들을 딕셔너리 형태로 변환하여 색인
docs = convert_files_to_docs(dir_path=doc_dir, clean_func=None)
print(f"data set len: {len(docs)}")

# 판례 insert sbert
document_store_rate_sb.write_documents(docs)
print(f"data insert len (rate_sb): {len(document_store_rate_sb.get_all_documents())}")
# 판례 insert bm25
document_store_rate_bm.write_documents(docs)
print(f"data insert len (rate_bm): {len(document_store_rate_bm.get_all_documents())}")


# 판례 sbert retriever / Dense Passage Retriever 설정
retriever_rate_sb = DensePassageRetriever(
    document_store=document_store_rate_sb,
    query_embedding_model="sentence-transformers/paraphrase-multilingual-mpnet-base-v2",  # 다국어에 어울리는 임베딩
    passage_embedding_model="sentence-transformers/paraphrase-multilingual-mpnet-base-v2",  # 다국어에 어울리는 임베딩
    use_gpu=True,
)
# 판례 bm25 retriever / BM25 Retriever 설정
retriever_rate_bm = BM25Retriever(document_store=document_store_rate_bm)


# 판례 sbert embedding_model에 맞춰서 임베딩
document_store_rate_sb.update_embeddings(retriever_rate_sb)


# 판례 sbert pipeline / Document Search Pipeline 설정
pipeline_rate_sb = DocumentSearchPipeline(retriever_rate_sb)
# 판례 bm25 pipeline / Document Search Pipeline 설정
pipeline_rate_bm = DocumentSearchPipeline(retriever_rate_bm)


# sbert 검색 함수
def search_rate_sb(query, k):
    res = pipeline_rate_sb.run(query, params={"Retriever": {"top_k": int(k)}})[
        "documents"
    ]
    return ([re.to_dict() for re in res]) if res else []


# bm25 검색 함수
def search_rate_bm(query, k):
    res = pipeline_rate_bm.run(query, params={"Retriever": {"top_k": int(k)}})[
        "documents"
    ]
    return ([re.to_dict() for re in res]) if res else []


# hybrid 검색 함수
def search_rate_hybrid(query, k):
    k = int(k)

    sbs = search_rate_sb(query=query, k=k)
    bms = search_rate_bm(query=query, k=k)

    return rrf(sbs, bms, k)


def rrf(sbs, bms, k):
    k = int(k)

    sb_names = [sb["meta"]["name"] for sb in sbs]
    bm_names = [bm["meta"]["name"] for bm in bms]

    scores = {
        name: {"sb": 0, "bm": 0, "total": 0} for name in list(set(sb_names + bm_names))
    }

    for idx, sb in enumerate(sbs):
        scores[sb["meta"]["name"]]["sb"] += 1 / (idx + 1)
        scores[sb["meta"]["name"]]["total"] += 1 / (idx + 1)
        scores[sb["meta"]["name"]]["content"] = sb["content"]

    for idx, bm in enumerate(bms):
        scores[bm["meta"]["name"]]["bm"] = 1 / (idx + 1)
        scores[bm["meta"]["name"]]["total"] = 1 / (idx + 1)
        scores[bm["meta"]["name"]]["content"] = bm["content"]

    scores = sorted(list(scores.items()), key=lambda x: -x[1]["total"])

    res = []
    for score in scores:
        res.append(
            {
                "content": score[1]["content"],
                "score": score[1]["total"],
                "meta": {"name": score[0]},
            }
        )

    return res if len(res) <= k else res[:k]


# 테스트
if __name__ == "__main__":
    print("bm")
    res = search_rate_bm("고속도로", 3)
    print(res)
    print([re["meta"]["name"] for re in res])
    print("\n\n\n")

    print("sb")
    res = search_rate_sb("고속도로", 3)
    print(res)
    print([re["meta"]["name"] for re in res])
    print("\n\n\n")

    print("hy")
    res = search_rate_hybrid("고속도로", 3)
    print(res)
    print([re["meta"]["name"] for re in res])
    print("\n\n\n")
