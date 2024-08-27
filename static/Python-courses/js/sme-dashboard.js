// Function to display the saved user data
function displayData() {
    const domain = localStorage.getItem('domain');
    const queryType = localStorage.getItem('queryType');
    const userMessage = localStorage.getItem('userMessage');
    const attachedFiles = localStorage.getItem('attachedFiles');

    document.getElementById('domain').textContent = domain || 'No data';
    document.getElementById('queryType').textContent = queryType || 'No data';
    document.getElementById('userMessage').textContent = userMessage || 'No data';
    document.getElementById('attachedFiles').textContent = attachedFiles || 'No files attached';
}

// Function to toggle the visibility of the answer container
function toggleAnswerContainer() {
    const answerContainer = document.querySelector('.answer-container');
    const toggleButton = document.getElementById('toggleButton');

    if (answerContainer.style.display === 'none' || answerContainer.style.display === '') {
        answerContainer.style.display = 'block';
        toggleButton.innerHTML = '<i class="fa-regular fa-xmark"></i>';
    } else {
        answerContainer.style.display = 'none';
        toggleButton.innerHTML = '<i class="fa-light fa-pen-to-square"></i> Answer';
    }
}

// Function to handle the submission of the mentor's answer
function submitAnswer() {
    const mentorAnswer = document.getElementById('mentorAnswer').value.trim();
    const mentorFileInput = document.getElementById('mentorFileInput');
    const answerFiles = mentorFileInput.files;

    if (mentorAnswer === '' && answerFiles.length === 0) {
        alert('Please provide an answer or attach files.');
        return;
    }

    // Collecting files and answer
    const formData = new FormData();
    formData.append('answer', mentorAnswer);
    
    for (let i = 0; i < answerFiles.length; i++) {
        formData.append('files', answerFiles[i]);
    }

    // Assuming you have a server endpoint to handle the POST request
    fetch('your-server-endpoint', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert('Answer submitted successfully!');
        // Optionally, clear the form after submission
        document.getElementById('mentorAnswer').value = '';
        document.getElementById('mentorFileInput').value = '';
        document.querySelector('.answer-container').style.display = 'none';
        document.getElementById('toggleButton').textContent = 'Answer';
    })
    .catch(error => {
        console.error('Error submitting answer:', error);
        alert('Failed to submit the answer.');
    });
}

// Add event listener to the Toggle button
document.getElementById('toggleButton').addEventListener('click', toggleAnswerContainer);

// Run displayData() on page load
document.addEventListener('DOMContentLoaded', displayData);
