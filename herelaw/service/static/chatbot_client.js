// 키보드 설정
var initialWindowHeight = window.innerHeight;
var initialScrollPosition = window.scrollY;

window.addEventListener('resize', function () {
    var currentWindowHeight = window.innerHeight;

    if (currentWindowHeight < initialWindowHeight) {
        // 키보드가 올라왔을 때
        var keyboardHeight = initialWindowHeight - currentWindowHeight;
        document.body.style.transform = 'translateY(-' + keyboardHeight + 'px)';
    } else {
        // 키보드가 내려갔을 때
        document.body.style.transform = 'translateY(0)';

        // 스크롤 위치 보정
        window.requestAnimationFrame(function () {
            window.scrollTo(0, initialScrollPosition);
        });
    }
});







// 스플래시 이미지 로딩
setTimeout(function () {
    var mainImageContainer = document.getElementById('main-image-container');
    if (mainImageContainer !== null) {
        mainImageContainer.style.display = 'none';
    }
    document.querySelector('.chat-container').style.display = 'none';
    document.getElementById('user-input').style.display = 'none';
}, 1000);


    // start-container 숨김
    setTimeout(() => {
    document.querySelector('.start-container').style.display = 'none';

    // 1초 후에 chat-container와 user-input 나타냄
    setTimeout(() => {
        document.querySelector('.chat-container').style.display = 'block';
        document.getElementById('user-input').style.display = 'block';
        startConversation();
    }, 1000);
});


const inputBox = document.getElementById('user-input');
const outputDiv = document.getElementById('output');
const questions = [
    // "지금 위치하신 지역입니다.</br>서비스를 계속하시려면 시작하기 버튼을 눌러주세요.",
    "사고나신 상황에 대해 자세히 설명해주세요</br>(ex: 위치, 도로형태, 진행방향, 가입하신 보험사 등)",
    "만약 상황설명이 어려우시다면, 질문을 드릴게요.</br> 무엇이 편한지 선택해주세요. ",
    "이제 3가지의 질문을 전달드릴게요. 답변을 작성해주세요.",
    "1. 어디서 사고가 났나요?(예; 고속도로, 교차로, 횡단보도,...)",
    "2. 내 차는 어떻게 가고 있었나요?(예: 직진, 후진, 주정차,..)",
    "3. 상대방은 어떻게 진행했나요??(예: 직진, 후진, 주정차,...)" ]

let isChatGptUsed = false;
let questionIndex = 0;
let conversation = []; // 질문과 사용자 응답을 저장하는 배열

//startConversation()

function startConversation(event) {
    // event.stopPropagation(); // 이벤트 전파 중지
    // 첫 번째 질문 출력
    setTimeout(() => {
        outputDiv.innerHTML += `<div class="bot-message">${questions[questionIndex]}</div>`;

        questionIndex++;
        // 두 번째 질문 1초 뒤에 자동 출력
        setTimeout(() => {
            outputDiv.innerHTML += `<div class="bot-message">${questions[questionIndex]}</div>`;
            questionIndex++;
            setTimeout(() => {
                const buttonContainer = document.createElement('div');
                buttonContainer.className = 'button-container';
                buttonContainer.innerHTML = `
          <button class="option-button_1"><img src="/static/images/질문_1.png"></br><span>질문을 주세요</span></button>
          <button class="option-button_2"><img src="/static/images/설명_1.png"></br><span>제가 직접 쓸게요</span></button>`;
                outputDiv.appendChild(buttonContainer);

                // option-button_1 클릭 이벤트 핸들러
                document.querySelector('.option-button_1').addEventListener('click', () => {
                    outputDiv.innerHTML += `<div class="bot-message">${questions[questionIndex]}</div>`;
                    questionIndex++;
                    scrollToBottom();
                    // 4번째 질문일 경우 1초 뒤에 5번째 질문 자동 출력
                    if (questionIndex === 3) {
                        setTimeout(() => {
                            outputDiv.innerHTML += `<div class="bot-message">${questions[questionIndex]}</div>`;
                            questionIndex++;
                            scrollToBottom();
                        }, 800);
                    }
                });
            }, 800);
        }, 800);
    }, 800);
}



// 엔터로 답변 전송
function submitOnEnter(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        document.getElementById('send-btn').click();
    }
}

// input 요소와 button 요소에 엔터 키 이벤트 핸들러를 추가합니다.
document.getElementById('user-input').addEventListener('keydown', submitOnEnter);
document.getElementById('send-btn').addEventListener('click', submitUserInput);


// option-button_2 클릭 이벤트 핸들러
document.getElementById('output').addEventListener('click', (event) => {
    isChatGptUsed = false;
    if (event.target.classList.contains('option-button_2')) {
        isChatGptUsed = true;
        const outputDiv = document.getElementById('output');
        // 첫 질문 출력
        outputDiv.innerHTML += `<div class="bot-message">상황을 최대한 자세히 입력해 주세요!</div>`;
        // 클릭 이벤트 처리k
        document.getElementById('send-btn').addEventListener('click', () => {
            GPTsendUserInput();
        });

        // option-button_2 클릭 시 질문 인덱스 증가 방지
        event.stopPropagation();
    }
});


function GPTsendUserInput() {
    const inputBox = document.getElementById('user-input');
    const outputDiv = document.getElementById('output');
    const userInput = inputBox.value.trim();
    if (userInput !== '') {
        //outputDiv.innerHTML += `<div class="user-message">${userInput}</div>`;
        showLoading();

        
        // Ajax 요청 보내기
        $.ajax({
            url: '/chat_chat',
            method: 'POST',
            data: JSON.stringify({ message: userInput }),
            contentType: 'application/json',
            success: function (response) {
                hideLoading();
                // const outputContainer = document.getElementById('output');
                // const lastBotMessage = outputContainer.getElementsByClassName('bot-message');
                // const buttonContainers = outputContainer.getElementsByClassName('toggle-button-container');
                // const lastButtonContainer = buttonContainers[buttonContainers.length - 1];
                // outputContainer.insertBefore(lastButtonContainer, lastBotMessage[lastBotMessage.length - 1].nextSibling);
                const botResponse = response.message;
                outputDiv.innerHTML += `<div class="bot-message">${botResponse}</div>`;
                inputBox.value = '';
                scrollToBottom();


            },
            error: function (error) {
                console.error(error);
                hideLoading();
            }
        });
    }
}




// input 요소와 button 요소에 엔터 키 이벤트 핸들러를 추가합니다.
document.getElementById('user-input').addEventListener('keydown', submitOnEnter);
document.getElementById('send-btn').addEventListener('keydown', submitOnEnter);





// 사용자 응답 제출
function submitUserInput(chat_cnt) {
    const userInput = document.getElementById('user-input').value.trim();
    if (userInput !== '') {
        outputDiv.innerHTML += `<div class="user-message">${userInput}</div>`;
        scrollToBottom();

        // 질문과 사용자 응답 저장
        conversation.push({
            question: questions[questionIndex - 1],
            answer: userInput 
        });
        
        // 다음 질문 표시
        console.log('->', isChatGptUsed);
        console.log('->', questionIndex, questions.length);
        if (!isChatGptUsed && questionIndex < questions.length) {
            // 챗봇 아닐 때
            outputDiv.innerHTML += `<div class="bot-message">${questions[questionIndex]}</div>`;
            scrollToBottom();
            questionIndex++;

            // 요소를 가져옵니다.
            const userMessageContainer = document.querySelector('.user-message');

            // 마지막 질문일 경우 사용자 응답 표시
            if (questionIndex === questions.length) {
                userMessageContainer.style.display = 'block';
                // 사용자 입력창 비활성화
                // inputBox.disabled = true;
            }
            // 사용자 입력창 초기화
            document.getElementById('user-input').value = '';
        } else {
            // 마지막 질문일 때 사용자 응답이 들어오면 사용자 응답 표시
            if (questionIndex === questions.length) {
                displayUserAnswers();
                // 사용자 입력창 초기화
                document.getElementById('user-input').value = '';
            }
            if (isChatGptUsed === true) {
                // 챗봇일 때
                if (chat_cnt === 2) {
                    console.log("챗봇일때 엔서가 떠야한다")
                    displayChatUserAnswers();
                  }
                  showLoading();
                //     // Ajax 요청 보내기
                //     console.log({ message: userInput });
                //     $.ajax({
                //       url: '/chatGPT',
                //       method: 'POST',
                //       data: { message: userInput },
                //       success: function(response) {
                //         hideLoading();

                //         const botResponse = response;
                //         outputDiv.innerHTML += `<div class="bot-message">${botResponse}</div>`;
                //         inputBox.value = '';
                //         scrollToBottom();
                //         // 서버 응답을 확인하여 버튼 표시 여부 결정
                //         if (response['guide']) {
                //             showGuideButtonGPT(response['guide']);
                //         } else {
                //             hideGuideButton();
                //         }
                //         if (response['insurance_number']) {
                //             showInsuranceButtonGPT(response['insurance_number']);
                //         } else {
                //             hideInsuranceButton();
                //         }
                //         if (response['agreement']) {
                //             showAgreementButtonGPT(response['agreement']);
                //         } else {
                //             hideAgreementButton();
                //         }
                //         if (response['res_gpt_sum2']) {
                //             showSummaryButtonGPT(response['res_gpt_sum2']);
                //         } else {
                //             hideSummaryButton();
                //         }
                //         if (response['rate']) {
                //             showRatioButtonGPT(response['rate']);
                //         } else {
                //             hideRatioButton();
                //         }
                //     },
                //       error: (error) => {
                //         console.error(error);
                //         hideLoading();
                //       }
                //     });
                //   }

            }
        }
    }
}










// 답변을 할 때마다 스크롤 맨 아래로 이동
function scrollToBottom() {
    let outputDiv = document.getElementById('output');
    outputDiv.scrollTop = outputDiv.scrollHeight;
}








function displayUserAnswers() {
    let userAnswers = conversation.map(item => `${item.answer}`);
    let userAnswersContainer = document.getElementById('user-answers-container');
    userAnswersContainer.innerHTML = `<div id="user-answers-container" class="user-answers-container">
    <div class="popup-message">
        <span class="answer">${userAnswers[0]}</span>에서 사고가 났어요. </br>
        본인은 <span class="answer">${userAnswers[1]}</span>으로 진행하고 있었는데, </br>
        상대방은 <span class="answer">${userAnswers[2]}</span>로 진행했어요.</br>

    </div>
</div>`;
    openUserAnswersPopup();
}

function displayChatUserAnswers(form_result, chat_cnt) {
    let chatUserAnswersContainer = document.getElementById('chat-user-answers-container');
    console.log("클릭됐당");
    
    if (chat_cnt === 2) {
    GPTopenUserAnswersPopup();
      chatUserAnswersContainer.innerHTML = form_result;

    } else {
      submitUserInput(); // chat_cnt가 0 또는 1일 경우 submitUserInput 함수 호출
    }
  }
  
  
// 챗챗레이어 팝업 열기
function GPTopenUserAnswersPopup() {
    let chatuserAnswersPopup = document.getElementById('chat-user-answers-popup');
    let chatuserAnswersContainer = document.getElementById('chat-user-answers-container');
    //let submitBtn = document.getElementById('submit-btn');
    chatuserAnswersContainer.style.display = 'block'; // 팝업 안의 컨테이너 보이기
    chatuserAnswersPopup.style.display = 'block';
    //submitBtn.style.display = 'block'; // Submit 버튼 표시
}

// 챗챗레이어 팝업 닫기
function closeUserAnswersPopup() {
    let chatuserAnswersPopup = document.getElementById('chat-user-answers-popup');
    let chatuserAnswersContainer = document.getElementById('chat-user-answers-container');
    let submitBtn = document.getElementById('submit-btn');
    chatuserAnswersContainer.style.display = 'none'; // 팝업 안의 컨테이너 숨기기
    chatuserAnswersPopup.style.display = 'none';
    submitBtn.style.display = 'none'; // Submit 버튼 숨기기
}




// 레이어 팝업 열기
function openUserAnswersPopup() {
    let userAnswersPopup = document.getElementById('user-answers-popup');
    let userAnswersContainer = document.getElementById('user-answers-container');
    //let submitBtn = document.getElementById('submit-btn');
    userAnswersContainer.style.display = 'block'; // 팝업 안의 컨테이너 보이기
    userAnswersPopup.style.display = 'block';
    //submitBtn.style.display = 'block'; // Submit 버튼 표시
}

// 레이어 팝업 닫기
function closeUserAnswersPopup() {
    let userAnswersPopup = document.getElementById('user-answers-popup');
    let userAnswersContainer = document.getElementById('user-answers-container');
    let submitBtn = document.getElementById('submit-btn');
    userAnswersContainer.style.display = 'none'; // 팝업 안의 컨테이너 숨기기
    userAnswersPopup.style.display = 'none';
    submitBtn.style.display = 'none'; // Submit 버튼 숨기기
}



// 파일 업로드 처리 함수
function handleFileUpload(event, uploadInput) {
    console.log('handleFileUpload 함수 호출됨');
    const file = uploadInput.files[0];
    if (file) {
        // 파일을 FileReader를 사용하여 읽습니다.
        const reader = new FileReader();
        reader.onload = function (e) {
            // 읽어들인 파일의 URL을 이미지 요소의 src에 할당하여 미리 보여줍니다.
            const previewImage = document.getElementById('preview-image');
            previewImage.src = e.target.result;
            console.log('File loaded successfully:', file.name);
        };

        reader.onerror = function (e) {
            console.error('Error occurred while reading the file:', e.target.error);
        };
        reader.readAsDataURL(file);
        console.log('File:', file);

        // 미리보기 이미지의 CSS 스타일을 수정하여 크기를 조정합니다.
        const previewImage = document.getElementById('preview-image');
        previewImage.style.display = 'block';
        previewImage.style.width = '300px';
    }
}




function sendConversation() {
    // 로딩 이미지 표시
    showLoading();
    // 대화 데이터를 JSON 형식으로 변환
    console.log(conversation)
    const jsonData = JSON.stringify({ conversation: conversation });

    // AJAX 요청 보내기
    $.ajax({
        url: '/role_chat',
        method: 'POST',
        data: jsonData,
        contentType: 'application/json',
        success: function (response) {
            window.location.href = '/result';
            // 로딩 이미지 숨김
            hideLoading();
            closeUserAnswersPopup();

        },
        error: function (response) {
            console.log('데이터를 서버에 전송하는데 실패했어요.');
            // 로딩 이미지 숨김
            hideLoading();
        },
    });
}


// 사용자 입력 전송
function sendUserInput() {
    const userInput = document.getElementById('user-input').value.trim();
    document.getElementById('user-input').value = '';
    return false; // 폼 제출 방지
}// SUBMIT 버튼 클릭 이벤트 핸들러
document.getElementById('submit-btn').addEventListener('click', sendConversation);






function showLoading() {
    // 로딩 이미지 표시
    var imageContainer = document.getElementById("image-container");
    imageContainer.style.display = "block";
}

function hideLoading() {
    // 로딩 이미지 숨김
    var imageContainer = document.getElementById("image-container");
    imageContainer.style.display = "none";
}
