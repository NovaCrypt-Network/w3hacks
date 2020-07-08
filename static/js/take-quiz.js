// Quiz Variables
let userAnswers = [];
let questionIndex = 0;
let quizLength = questions.length;

// HTML Tags
const quizContainer = document.getElementById("quiz-container");
const questionCountTag = document.getElementById("question-count");
const questionTag = document.getElementById("question");
const answersTag = document.getElementById("answers");

// onInit -> boolean -> true if function was called on initalization
function getQuestion(onInit) {
  // If this was called from submitting an answer
  if (!onInit) {
    // Get input node
    let answer = document.querySelector("input[type='radio']:checked");

    // If the user selected an answer
    if (answer) {
      userAnswers.push(answer.value); // Add the answer to answers
    }
    // If the user selected an answer
    else {
      alert("You must select a question."); // Alert an error
      return; // Don't move to the next question
    }
  }

  let question = questions[questionIndex];

  // End of quiz
  if (question == undefined) {
    quizContainer.innerHTML = `
      <div class='mb-4'>
        <strong>Congratulations! You finished the quiz!</strong>
        <p>Click below to see your results, and get feedback on what you should work on in the future!</p>
      </div>
      <div>
        <a class='solid-cta-button' href='../quiz-results/?id=" + quiz_id + "'>See Results</a>
      </div>
    `;

    // Creating completed quiz exercise
    fetch("/create-completed-quiz-exercise/", {
      method: "POST",
      body: JSON.stringify({
        quiz_exercise_id: quiz_id,
        userAnswers: userAnswers
      })
    })

    return;
  }

  // Setting question counter to current question count
  questionCountTag.innerHTML = "Question " + (questionIndex + 1).toString() + "/" + quizLength.toString();

  // Displaying question on HTML
  questionTag.innerHTML = question.question;

  // Adding each answer to HTML though iteration
  answersTag.innerHTML = ""; // Clearing answers before adding again
  for (answer of question.answers) {
    answersTag.innerHTML += "<li class='answer'><input type='radio' name='answer' value='" + answer + "'>" + answer + "</li>";
  }

  questionIndex++;
}

getQuestion(true); // To start things off
