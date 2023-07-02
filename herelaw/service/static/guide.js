//////////////////// 스플래시 이미지 로딩
// setTimeout(function () {
//   var mainImageContainer = document.getElementById("main-image-container");
//   if (mainImageContainer !== null) {
//     mainImageContainer.style.display = "none";
//   }
//   document.querySelector(".chat-container").style.display = "none";
//   document.getElementById("user-input").style.display = "none";
// }, 1500);

//////////////////// 팝업창
function HighwayPopup() {
  const highwayOverlay = document.getElementById("highway-overlay");
  highwayOverlay.style.display = "flex";

  const closeButton = highwayOverlay.querySelector(".close-button");
  if (closeButton) {
    closeButton.addEventListener("click", () => {
      highwayOverlay.style.display = "none";
    });
  }
}

function CarPopup() {
  const carOverlay = document.getElementById("car-overlay");
  carOverlay.style.display = "flex";

  const closeButton = carOverlay.querySelector(".close-button");
  if (closeButton) {
    closeButton.addEventListener("click", () => {
      carOverlay.style.display = "none";
    });
  }
}

function HumanPopup() {
  const humanOverlay = document.getElementById("human-overlay");
  humanOverlay.style.display = "flex";

  const closeButton = humanOverlay.querySelector(".close-button");
  if (closeButton) {
    closeButton.addEventListener("click", () => {
      humanOverlay.style.display = "none";
    });
  }
}

function BicyclePopup() {
  const bicycleOverlay = document.getElementById("bicycle-overlay");
  bicycleOverlay.style.display = "flex";

  const closeButton = bicycleOverlay.querySelector(".close-button");
  if (closeButton) {
    closeButton.addEventListener("click", () => {
      bicycleOverlay.style.display = "none";
    });
  }
}

function MotorcyclePopup() {
  const motorcycleOverlay = document.getElementById("motorcycle-overlay");
  motorcycleOverlay.style.display = "flex";

  const closeButton = motorcycleOverlay.querySelector(".close-button");
  if (closeButton) {
    closeButton.addEventListener("click", () => {
      motorcycleOverlay.style.display = "none";
    });
  }
}

//////////////////// 팝업버튼
function showPopup_2(trafficOffensePopup) {
  var popup_1 = document.getElementById("trafficOffensePopup");
  popup_1.style.display = "block";
}

function showPopup_1(emergencyTowingPopup) {
  var popup_2 = document.getElementById("emergencyTowingPopup");
  popup_2.style.display = "block";
}

function hidePopup_2(trafficOffensePopup) {
  var popup_1 = document.getElementById("trafficOffensePopup");

  popup_1.style.display = "none";
}

function hidePopup_1(emergencyTowingPopup) {
  var popup_2 = document.getElementById("emergencyTowingPopup");

  popup_2.style.display = "none";
}

//////////////////// 도와줘요 히어로 버튼
function send_data(accident_category) {
  // 서버로 전송할 데이터 준비
  let latitude = null; // 위도
  let longitude = null; // 경도

  // 위도 경도
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      latitude = position.coords.latitude; // 위도
      longitude = position.coords.longitude; // 경도

// 폼 데이터
var formData = new FormData();

// 사진
for (let i = 1; i <= 5; i++) {
  var fileInput = document.getElementById("photoUpload" + i);
  if (fileInput && fileInput.files && fileInput.files.length > 0) {
    formData.append("file", fileInput.files[0]); // Append the file to the FormData object
    break; // 첫 번째로 발견된 파일만 추가하고 반복문 종료
  }
}
      // 차도 유형
      var dataToSend = {
        road: accident_category, // 서버로 전송할 값
        latitude: latitude,
        longitude: longitude,
      };
      formData.append("data", JSON.stringify(dataToSend)); // Append the data to the FormData object

      console.log(formData);

      // AJAX 요청 보내기
      $.ajax({
        url: "/client_keyword",
        type: "POST",
        data: formData,
        contentType: false,
        processData: false,
        success: function(response) {
          console.log("서버에 값 전송 성공");
          window.location.href = "/chatbot";
        },
        error: function(error) {
          console.error("서버에 값 전송 실패:", error);
        },
      });
    });
  } else {
    latitude = null; // 위도
    longitude = null; // 경도
  }
}


// 버튼 클릭
var highwayButton = document.getElementById("highway_button");
highwayButton.addEventListener("click", function () {
  send_data("고속도로");
});

var carButton = document.getElementById("car_button");
carButton.addEventListener("click", function () {
  send_data("차 대 차");
});

var biButton = document.getElementById("bicycle_button");
biButton.addEventListener("click", function () {
  send_data("차 대 자전거");
});

var huButton = document.getElementById("human_button");
huButton.addEventListener("click", function () {
  send_data("차 대 사람");
});

var moButton = document.getElementById("motorcycle_button");
moButton.addEventListener("click", function () {
  send_data("차 대 이륜차");
});
