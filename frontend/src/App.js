import React, { useState } from "react";
import './App.css';

import Keycloak from "keycloak-js";

let initOptions = {
  url: 'http://localhost:8080/',
  realm: 'myrealm',
  clientId: 'frontend',
}

let kc = new Keycloak(initOptions);

kc.init({
  onLoad: 'login-required', // Supported values: 'check-sso' (default), 'login-required'
  checkLoginIframe: true
}).then((auth) => {
  if (!auth) {
    window.location.reload();
  }
  else {
    // alert("Authenticated");
    // alert(auth)
    // alert(kc)
    console.log(kc.token)

    kc.onTokenExpired = () => {
      // alert('token expired')
    }
  }
}, () => {
  // alert("Authentication Failed");
});

var counter = 0;
var timer = 30;
var currentKey;
var timerInterval = 0;

// const instruction = document.getElementById('instruction');
// const counterDisplay = document.getElementById('counter');


  document.addEventListener('keydown', function(event) {

    if(event.key === 'Enter' && timer === 30) {
      startGame();

    }else if (event.key === currentKey) {
      counter++;
      document.getElementById('counter').innerHTML = `Counter: ${counter}`;

      currentKey = generateRandomKey();
      document.getElementById('instruction').innerHTML = `Press '${currentKey}' to increase the counter`;
    }
  });

function generateRandomKey() {
  return String.fromCharCode(97 + Math.floor(Math.random() * 26)); // A-Z
}

function startGame() {
  counter = 0;
  currentKey = generateRandomKey();
  document.getElementById('instruction').innerHTML = `Press '${currentKey}' to increase the counter`;

  timerInterval = setInterval(function() {
    timer--;
    document.getElementById("timerDisplay").innerHTML = `Time: ${timer}`;
    if(timer === 0) endGame();
  }, 1000);

}

function endGame() {
    clearInterval(timerInterval);

    // const username = kc.loadUserInfo();
    fetch('http://localhost:5000/submit_score', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          token: kc.token,
          score: counter
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
        document.getElementById('instruction').innerHTML = `Time's up! Your score is ${counter}. Try again? Press 'Enter' to start`;
        currentKey = null;
        counter = 0;
        timer = 30;
        document.getElementById("timerDisplay").innerHTML = "Time: 30";
        document.getElementById('counter').innerHTML = 'Counter: 0';
    });
  }


function App() {
  const [leaderboardItems, setLeaderboardItems] = useState([]);

  const showLeaderboard = () => {
    fetch(`http://localhost:5000/leaderboard/${kc.token}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    })
    .then(response => response.json())
    .then(data => {
      setLeaderboardItems(data.leaderboard);
    });
  }

  return (
    <div className="App">
      <h1 id="instruction">Press 'Enter' to start the timer</h1>
      <div id="counter">Counter: 0</div>
      <h2 id="timerDisplay">Time: 30</h2>
      <button onClick={showLeaderboard}>Check Leaderboard</button>

      <br></br>
      <br></br>
      <button onClick={() => {kc.logout()}}>Logout</button>
      <br></br>
      <br></br>
      <div className="container">
        { leaderboardItems.map((item) => (
          <div>
            <h3>{item.name} - {item.score} ({item.datetime.split(" GMT")[0]})</h3>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;