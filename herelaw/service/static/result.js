function RatePopup() {
  const rateOverlay = document.getElementById("ratio-overlay");
  rateOverlay.style.display = "flex";

  const closeButton = rateOverlay.querySelector(".close-button");
  if (closeButton) {
    closeButton.addEventListener("click", () => {
      rateOverlay.style.display = "none";
    });
  }
}

function AgreementPopup() {
  const agreementOverlay = document.getElementById("agreement-overlay");
  agreementOverlay.style.display = "flex";

  const closeButton = agreementOverlay.querySelector(".close-button");
  if (closeButton) {
    closeButton.addEventListener("click", () => {
      agreementOverlay.style.display = "none";

      const agreementContent = document.getElementById("agreement-image");
      agreementContent.innerHTML = ""; // 이미지 제거
    });
  }
  fetch("/get_file_name")
    .then((response) => response.text())
    .then((file_name) => {
      const imageUrl = "/static/reports/" + file_name;
      const imageElement = document.createElement("img");
      imageElement.src = imageUrl;
      imageElement.alt = "과실심의분쟁위원회 이미지";
      imageElement.width = 360;
      imageElement.addEventListener("click", () =>
        showOriginalImage(file_name)
      );
      const agreementContent = document.getElementById("agreement-content");
      agreementContent.innerHTML = ""; // 이미지 요소 초기화
      agreementContent.appendChild(imageElement);
      agreementContent.style.display = "block";
    })
    .catch((error) => {
      console.error("데이터 가져오기 실패:", error);
    });

  // ...
}

const downloadButton = document.getElementById("download-button");
const agreementImage = document.getElementById("agreement-image");

downloadButton.addEventListener("click", () => {
  const link = document.createElement("a");
  link.href = agreementImage.src;
  link.download = "과실심의분쟁위원회.png";
  link.click();
});

function showOriginalImage(name) {
  const imageUrl = "/static/reports/" + name; // 이미지 파일의 경로를 설정해야 합니다.
  const popupWindow = window.open("", "_blank", "width=800, height=600");
  const popupDocument = popupWindow.document;
  popupDocument.write(
    '<html><head><title>원본 이미지</title></head><body style="margin: 0; display: flex; justify-content: center; align-items: center;"><img src="' +
      imageUrl +
      '" style="max-width: 100%; max-height: 100%; cursor: pointer;"></body></html>'
  );
  popupDocument.close();

  const imageElement = popupDocument.querySelector("img");
  imageElement.onclick = function () {
    popupWindow.close(); // 이미지를 클릭하면 팝업 창이 닫히도록 설정
  };
}

function LawPopup() {
  const lawOverlay = document.getElementById("law-overlay");
  lawOverlay.style.display = "flex";

  const closeButton = lawOverlay.querySelector(".close-button");
  if (closeButton) {
    closeButton.addEventListener("click", () => {
      lawOverlay.style.display = "none";
    });
  }
}

function LawerPopup() {
  const lawerOverlay = document.getElementById("lawer-overlay");
  lawerOverlay.style.display = "flex";

  const closeButton = lawerOverlay.querySelector(".close-button");
  if (closeButton) {
    closeButton.addEventListener("click", () => {
      lawerOverlay.style.display = "none";
    });
  }
}
