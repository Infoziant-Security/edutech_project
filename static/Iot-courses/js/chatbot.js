let currentQuestion = 0;
let domain = '';
let queryType = '';
let userMessage = '';
let otherInput = '';
let selectedFiles = []; // Array to store selected files

const questions = [
    {
        question: "Please choose the subject area of your query",
        options: ["AR/VR (Augmented Reality/Virtual Reality)","Cloud Computing","Cybersecurity","Blockchain","Web Development", "Mobile Development", "Data Science", "AI/ML", "Other"]
    },
    {
        question: "What type of query do you have?",
        options: ["General Query", "Project Support Request","Technical Assistance","Mentorship/Guidance", "Other"]
    },
    {
        question: "Enter your message:",
        options: []
    },
    {
        question: "Attach files (optional):",
        options: []
    }
];

function displayQuestion() {
    const questionBox = document.getElementById("questionBox");
    const current = questions[currentQuestion];

    let optionsHTML = '';
    if (current.options.length > 0) {
        optionsHTML = current.options.map(option => 
            `<div>
                <input type="radio" name="option" value="${option}" onclick="handleOptionClick('${option}')"> ${option}
            </div>`
        ).join('');
    }

    questionBox.innerHTML = `
        <div class="question-bg">${current.question}</div>
        <div id="error" class="error" style="display: none;">Please provide an answer.</div>
        <div class="options-bg">${optionsHTML}</div>
    `;

    if (currentQuestion === 2) {
        document.getElementById("userInput").style.display = 'block';
        document.getElementById("fileInput").style.display = 'none';
    } else if (currentQuestion === 3) {
        document.getElementById("userInput").style.display = 'none';
        document.getElementById("fileInput").style.display = 'block';
    } else {
        document.getElementById("userInput").style.display = 'none';
        document.getElementById("fileInput").style.display = 'none';
    }
}

function handleOptionClick(option) {
    const userInput = document.getElementById("userInput");
    if (option === 'Other') {
        userInput.style.display = 'block';
        userInput.placeholder = "Please specify";
    } else {
        userInput.style.display = 'none';
    }
}

document.getElementById("fileInput").addEventListener("change", function(event) {
    const files = event.target.files;
    for (let i = 0; i < files.length; i++) {
        selectedFiles.push(files[i]);
        displayFile(files[i]);
    }
});

function displayFile(file) {
    const fileList = document.getElementById("fileList");
    const fileItem = document.createElement("div");
    fileItem.className = "file-item";
    fileItem.textContent = file.name;
    fileList.appendChild(fileItem);
}

function handleSubmit() {
    const userInput = document.getElementById("userInput").value.trim();
    const error = document.getElementById("error");

    if (currentQuestion === 0 || currentQuestion === 1) {
        const selectedOption = document.querySelector('input[name="option"]:checked');
        if (!selectedOption) {
            error.style.display = 'block';
            return;
        }

        if (selectedOption.value === 'Other') {
            if (userInput === '') {
                error.style.display = 'block';
                return;
            }
            otherInput = userInput;
        }

        error.style.display = 'none';

        if (currentQuestion === 0) {
            domain = selectedOption.value === 'Other' ? otherInput : selectedOption.value;
        } else if (currentQuestion === 1) {
            queryType = selectedOption.value === 'Other' ? otherInput : selectedOption.value;
        }
    } else if (currentQuestion === 2) {
        if (userInput === '') {
            error.style.display = 'block';
            return;
        }

        error.style.display = 'none'; 
        userMessage = userInput;
    } else if (currentQuestion === 3) {
        // No further validation needed for file upload question
    }

    document.getElementById("userInput").value = '';

    currentQuestion++;
    if (currentQuestion < questions.length) {
        displayQuestion();
    } else {
        displayResponses();
    }
}

function displayResponses() {
    const questionBox = document.getElementById("questionBox");
    questionBox.innerHTML = `
    <div class="thanks-bg">Thank you! Your query has been submitted. Our experts will get back to you soon.</div>
    <div class="responses-bg">
    <div>Your Responses:</div>
        <div>Domain: ${domain}</div>
        <div>Query Type: ${queryType}</div>
        <div>Message: ${userMessage}</div>
        <div>Attached Files: ${selectedFiles.map(file => file.name).join(', ')}</div>
    </div>
    `;

    const submitButton = document.querySelector('.input-area button');
    submitButton.textContent = "Start Over";
    submitButton.onclick = startAgain;
    document.getElementById("fileInput").style.display = 'none';
    document.getElementById("fileList").innerHTML = ''; // Clear file list
    selectedFiles = []; // Reset the selected files array
}

function startAgain() {
    currentQuestion = 0;
    domain = '';
    queryType = '';
    userMessage = '';
    otherInput = '';
    selectedFiles = [];
    displayQuestion();

    const submitButton = document.querySelector('.input-area button');
    submitButton.textContent = "Send";
    submitButton.onclick = handleSubmit;
}

document.addEventListener("DOMContentLoaded", displayQuestion);


// let currentQuestion = 0;
// let domain = '';
// let queryType = '';
// let userMessage = '';
// let otherInput = '';
// let attachedFiles = []; // To store attached files

// const questions = [
//     {
//         question: "Please choose the subject area of your query",
//         options: ["AR/VR (Augmented Reality/Virtual Reality)", "Cloud Computing", "Cybersecurity", "Blockchain", "Web Development", "Mobile Development", "Data Science", "AI/ML", "Other"]
//     },
//     {
//         question: "What type of query do you have?",
//         options: ["General Query", "Project Support Request", "Technical Assistance", "Mentorship/Guidance", "Other"]
//     },
//     {
//         question: "Enter your message:",
//         options: []
//     },
//     {
//         question: "Do you want to attach any images/documents/videos?",
//         options: []
//     }
// ];

// function displayQuestion() {
//     const questionBox = document.getElementById("questionBox");
//     const current = questions[currentQuestion];

//     let optionsHTML = '';
//     if (current.options.length > 0) {
//         optionsHTML = current.options.map(option => 
//             `<div>
//                 <input type="radio" name="option" value="${option}" onclick="handleOptionClick('${option}')"> ${option}
//             </div>`
//         ).join('');
//     }

//     questionBox.innerHTML = `
//         <div class="question-bg">${current.question}</div>
//         <div id="error" class="error" style="display: none;">Please provide an answer.</div>
//         <div class="options-bg">${optionsHTML}</div>
//     `;

//     if (currentQuestion === 2) {
//         document.getElementById("userInput").style.display = 'block';
//         document.getElementById("fileInput").style.display = 'none';
//     } else if (currentQuestion === 3) {
//         document.getElementById("userInput").style.display = 'none';
//         document.getElementById("fileInput").style.display = 'block';
//     } else {
//         document.getElementById("userInput").style.display = 'none';
//         document.getElementById("fileInput").style.display = 'none';
//     }
// }

// function handleOptionClick(option) {
//     const userInput = document.getElementById("userInput");
//     if (option === 'Other') {
//         userInput.style.display = 'block';
//         userInput.placeholder = "Please specify";
//     } else {
//         userInput.style.display = 'none';
//     }
// }

// function handleSubmit() {
//     const userInput = document.getElementById("userInput").value.trim();
//     const fileInput = document.getElementById("fileInput");
//     const error = document.getElementById("error");

//     if (currentQuestion === 0 || currentQuestion === 1) {
//         const selectedOption = document.querySelector('input[name="option"]:checked');
//         if (!selectedOption) {
//             error.style.display = 'block';
//             return;
//         }

//         if (selectedOption.value === 'Other') {
//             if (userInput === '') {
//                 error.style.display = 'block';
//                 return;
//             }
//             otherInput = userInput;
//         }

//         error.style.display = 'none';

//         if (currentQuestion === 0) {
//             domain = selectedOption.value === 'Other' ? otherInput : selectedOption.value;
//         } else if (currentQuestion === 1) {
//             queryType = selectedOption.value === 'Other' ? otherInput : selectedOption.value;
//         }
//     } else if (currentQuestion === 2) {
//         if (userInput === '') {
//             error.style.display = 'block';
//             return;
//         }

//         error.style.display = 'none'; 
//         userMessage = userInput;
//     } else if (currentQuestion === 3) {
//         if (fileInput.files.length === 0) {
//             error.style.display = 'block';
//             return;
//         }

//         error.style.display = 'none';

//         // Capture attached files
//         attachedFiles = Array.from(fileInput.files);
//     }

//     document.getElementById("userInput").value = '';
//     fileInput.value = ''; // Clear the file input field

//     currentQuestion++;
//     if (currentQuestion < questions.length) {
//         displayQuestion();
//     } else {
//         saveData();
//     }
// }

// function saveData() {
//     localStorage.setItem('domain', domain);
//     localStorage.setItem('queryType', queryType);
//     localStorage.setItem('userMessage', userMessage);
    
//     const fileNames = attachedFiles.map(file => file.name).join(', ');
//     localStorage.setItem('attachedFiles', fileNames);

//     displayThankYouMessage();
// }

// function displayThankYouMessage() {
//     const questionBox = document.getElementById('questionBox');
//     questionBox.innerHTML = `
//         <div class="thanks-bg">Thank you! Your query has been submitted. Our experts will get back to you soon.</div>
//     `;
    
//     const submitButton = document.querySelector('.input-area button');
//     submitButton.textContent = "Start Over";
//     submitButton.onclick = startAgain;
//     document.getElementById("userInput").style.display = 'none';
//     document.getElementById("fileInput").style.display = 'none';
// }

// function startAgain() {
//     currentQuestion = 0;
//     domain = '';
//     queryType = '';
//     userMessage = '';
//     otherInput = '';
//     attachedFiles = [];
//     displayQuestion();

//     const submitButton = document.querySelector('.input-area button');
//     submitButton.textContent = "Send";
//     submitButton.onclick = handleSubmit;
// }

// document.addEventListener("DOMContentLoaded", displayQuestion);
