import 'react';
import { useState } from 'react';

const ChallengeChoices = ({ challenge, showExplanation = false }) => {
  const [selectedOption, setSelectedOption] = useState(null);
  const [shouldShowExplanation, setShouldShowExplanation] = useState(showExplanation);

  const options = typeof challenge.options === 'string' ? JSON.parse(challenge.options) : challenge.options;

  // handle option select. if the user has already selected an option, then dont allow them to select another option.
  const handleOptionSelect = (index) => {
    if (selectedOption !== null) return;
    setSelectedOption(index);
    setShouldShowExplanation(true);
  };

  // style the options based on selection and correctness
  const styleOptionClass = (index) => {
    if (selectedOption === null) return 'option';

    if (index === challenge.correct_answer_id) {
      return 'option correct';
    }
    if (selectedOption === index && index !== challenge.correct_answer_id) {
      return 'option incorrect';
    }

    return 'option';
  };

  return (
    <div className='challenge-display'>
      <p>
        <strong>Difficulty</strong>: {challenge.difficulty}
      </p>
      <p className='challenge-title'>{challenge.title}</p>
      <div className='options'>
        {options.map((option, index) => (
          <div className={styleOptionClass(index)} key={index} onClick={() => handleOptionSelect(index)}>
            {String.fromCharCode(65 + index)}. {option}
          </div>
        ))}
      </div>
      {shouldShowExplanation && selectedOption !== null && (
        <div className='explanation'>
          <h4>Explanation</h4>
          <p>{challenge.explanation}</p>
        </div>
      )}
    </div>
  );
};

export default ChallengeChoices;
