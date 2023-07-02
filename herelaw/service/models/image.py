from PIL import Image, ImageDraw, ImageFont
import folium


def add_images_to_image(background_image, image_paths, start_positions, end_positions):
    for image_path, start_position, end_position in zip(
        image_paths, start_positions, end_positions
    ):
        image = Image.open(image_path).convert("RGBA")
        image = image.resize(
            (end_position[0] - start_position[0], end_position[1] - start_position[1])
        )

        background_image.paste(image, start_position, image)

    return background_image


def add_text_and_images_to_image(
    image_path,
    texts,
    font_path,
    max_font_size,
    text_color,
    image_paths,
    start_positions,
    end_positions,
    name,
):
    # 이미지 열기
    image = Image.open(image_path).convert("RGB")

    # 이미지에 텍스트 추가를 위한 Draw 객체 생성
    draw = ImageDraw.Draw(image)

    for text_info in texts:
        # 텍스트 정보 추출
        text = text_info["text"]
        start_position = text_info["start_position"]
        end_position = text_info["end_position"]

        # 폰트 크기 초기값
        font_size = max_font_size

        # 폰트 로드
        font = ImageFont.truetype(font_path, font_size)

        # 텍스트 크기 초기값
        text_width, text_height = draw.textsize(text, font=font)

        # 텍스트 크기를 조절하여 이미지 안에 맞도록 함
        while font_size > 20 and (
            text_width > (end_position[0] - start_position[0])
            or text_height > (end_position[1] - start_position[1])
        ):
            font_size -= 1
            font = ImageFont.truetype(font_path, font_size)
            text_width, text_height = draw.textsize(text, font=font)

        # 텍스트 위치 설정
        x, y = start_position

        # 텍스트를 이미지에 그리기
        lines = []
        words = text.split(" ")
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            test_width, _ = draw.textsize(test_line, font=font)
            if test_width <= (end_position[0] - start_position[0]):
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)

        line_height = font.getsize("A")[1]  # 폰트의 높이를 기준으로 세로 간격 설정
        total_text_height = line_height * len(lines)
        y += (end_position[1] - start_position[1] - total_text_height) // 2  # 세로 중앙 정렬

        for line in lines:
            line_width, _ = draw.textsize(line, font=font)
            line_position = (
                x + (end_position[0] - start_position[0] - line_width) // 2,
                y,
            )
            draw.text(line_position, line, font=font, fill=text_color)
            y += line_height

    # 이미지 추가
    image = add_images_to_image(image, image_paths, start_positions, end_positions)

    # 결과 이미지 저장
    image.save(f"herelaw/service/static/reports/{name}")

    # print("텍스트와 이미지가 이미지에 추가되었습니다!")


def report_input(data, final_position, final_weather, current_date, name, lat, lng):
    image_path = f"herelaw/service/data/교통사고신속처리협의서.PNG"
    texts = [
        {"text": f"{data}", "start_position": (107, 716), "end_position": (700, 763)},
        {
            "text": f"{current_date}",
            "start_position": (145, 66),
            "end_position": (419, 66),
        },
        {
            "text": f"{final_position}",
            "start_position": (626, 65),
            "end_position": (898, 65),
        },
        {
            "text": f"{final_weather}",
            "start_position": (1048, 64),
            "end_position": (1235, 64),
        },
    ]

    font_path = "herelaw/service/data/OdBestFreind.ttf"
    max_font_size = 48  # 최대 폰트 크기
    text_color = (0, 0, 0)  # 텍스트 색상 (RGB 값)
    image_paths = [
        f"herelaw/service/uploads/pictures/{name}", "herelaw/service/data/약도.PNG"
    ]
    start_positions = [
        (85, 301), (745, 617)
    ]
    end_positions = [
        (572, 505), (1265, 783)
    ]

    add_text_and_images_to_image(
        image_path,
        texts,
        font_path,
        max_font_size,
        text_color,
        image_paths,
        start_positions,
        end_positions,
        name,
    )
