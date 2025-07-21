import { useState } from 'react';
import './index.scss';

const App = () => {
  const [hours, setHours] = useState('00');
  const [minutes, setMinutes] = useState('00');
  
  const padTime = (value) => {
    return value.toString().padStart(2, '0');
  };

  const handleHoursUp = () => {
    const newHours = (parseInt(hours, 10) + 1) % 24;
    console.log(newHours)
    setHours(padTime(newHours));
  };

  const handleHoursDown = () => {
    const newHours = (parseInt(hours, 10) - 1 + 24) % 24;
    setHours(padTime(newHours));
  };

  const handleMinutesUp = () => {
    const newMinutes = (parseInt(minutes, 10) + 1) % 60;
    setMinutes(padTime(newMinutes));
  };

  const handleMinutesDown = () => {
    const newMinutes = (parseInt(minutes, 10) - 1 + 60) % 60;
    setMinutes(padTime(newMinutes));
  };

  return (
    <div id="ClockUpdater" className="container">
      <div className="row">
        <button
          id="hours-up-button"
          className="btn btn-outline-primary col"
          onClick={handleHoursUp}
        >
          &uarr;
        </button>

        <button
          id="minutes-up-button"
          className="btn btn-outline-primary col"
          onClick={handleMinutesUp}
        >
          &uarr;
        </button>
      </div>

      <div className="row">
        <div id="clock" className="badge badge-primary col">
          {`${hours}:${minutes}`}
        </div>
      </div>

      <div className="row">
        <button
          id="hours-down-button"
          className="btn btn-outline-primary col"
          onClick={handleHoursDown}
        >
          &darr;
        </button>

        <button
          id="minutes-down-button"
          className="btn btn-outline-primary col"
          onClick={handleMinutesDown}
        >
          &darr;
        </button>
      </div>
    </div>
  );
};

export default App;
