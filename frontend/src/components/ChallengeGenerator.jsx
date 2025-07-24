import 'react';
import { useState, useEffect } from 'react';
import ChallengeChoices from './ChallengeChoices.jsx';
import { useApi } from '../servicesHook.js';
import { ToastContainer, toast } from 'react-toastify';

const ChallengeGenerator = () => {
  const [challenge, setChallenge] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  // const [error, setError] = useState(null);
  const [difficulty, setDifficulty] = useState('easy');
  const [quota, setQuota] = useState(null);
  const { makeRequest } = useApi();

  useEffect(() => {
    fetchQuota();
  }, []);

  const fetchQuota = async () => {
    try {
      const data = await makeRequest('quota');
      setQuota(data);
      console.log('QUOTA', data);
    } catch (err) {
      console.log(err);
    }
  };

  const generateChallenge = async () => {
    setIsLoading(true);
    // setError(null);

    try {
      const data = await makeRequest('generate-challenge', {
        method: 'POST',
        body: JSON.stringify({ difficulty }),
      });
      setChallenge(data);
      fetchQuota();
    } catch (err) {
      // setError(err.message || 'Failed to generate challenge.');
      toast.error(err.message || '❌ Failed to generate challenge.');
    } finally {
      setIsLoading(false);
    }
  };

  // This function is used to get the next reset time for the quota.

  const getNextResetTime = () => {
    if (!quota?.last_reset_data) return null;
    const resetDate = new Date(quota.last_reset_data);
    // we are getting the prev reset date and adding 24 hrs to it.
    resetDate.setHours(resetDate.getHours() + 24);
    return resetDate;
  };

  return (
    <div className='challenge-container'>
      <div className='challenge-generator-container'>
        <div className='quota-display'>
          <p>Challenges remaining today: {quota?.quota_remaining || 0}</p>
          {quota?.quota_remaining === 0 && <p>Next reset: {getNextResetTime()?.toLocaleString()}</p>}
        </div>
        <div className='difficulty-selector'>
          <label htmlFor='difficulty'>Select Difficulty</label>
          <select
            id='difficulty'
            value={difficulty}
            onChange={(e) => setDifficulty(e.target.value)}
            disabled={isLoading}
          >
            <option value='easy'>Easy</option>
            <option value='medium'>Medium</option>
            <option value='hard'>Hard</option>
          </select>
        </div>

        <button
          onClick={generateChallenge}
          disabled={isLoading || quota?.quota_remaining === 0}
          className='generate-button'
        >
          {isLoading ? 'Generating...' : 'Generate Challenge'}
        </button>
      </div>
      {challenge && <ChallengeChoices challenge={challenge} />}
      <ToastContainer />
    </div>
  );
};

export default ChallengeGenerator;
