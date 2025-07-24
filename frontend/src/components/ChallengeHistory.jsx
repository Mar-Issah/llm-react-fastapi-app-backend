import 'react';
import { useState, useEffect } from 'react';
import ChallengeChoices from './ChallengeChoices.jsx';
import { useApi } from '../servicesHook.js';
import { ToastContainer, toast } from 'react-toastify';

const ChallengeHistory = () => {
  const { makeRequest } = useApi();
  const [history, setHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const data = await makeRequest('my-history');
      console.log(data);
      setHistory(data.challenges);
    } catch (err) {
      setError(err);
      toast.error(err.message || '❌ Failed to load history.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className='history-panel'>
      <h2>History</h2>
      {history.length === 0 ? (
        <>
          <p>{isLoading ? 'Fetching History...' : 'No challenge history'}</p>
          {error && (
            <button className='generate-button' onClick={fetchHistory}>
              Retry
            </button>
          )}
        </>
      ) : (
        <div className='history-list'>
          {history.map((challenge) => {
            return <ChallengeChoices challenge={challenge} key={challenge.id} showExplanation />;
          })}
        </div>
      )}
      <ToastContainer />
    </div>
  );
};

export default ChallengeHistory;
