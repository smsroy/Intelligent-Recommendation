import "./App.css";
import React, { useState, useEffect } from "react";

function App() {
  const [data, setData] = useState([{}]);

  useEffect(() => {
    fetch("/reco")
      .then((res) => res.json())
      .then((data) => {
        setData(data);
        console.log(data);
      });
  }, []);
  return (
    <div>
      <header className="App-header">
        {typeof data.reco === "undefined" ? (
          <p>Loading ... </p>
        ) : (
          data.reco.map((rec, i) => <p key={i}> {rec}</p>)
        )}
      </header>
    </div>
  );
}

export default App;
