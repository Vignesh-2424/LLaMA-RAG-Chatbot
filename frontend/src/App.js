import './App.css';
import Upload from './components/Upload';
import Chat from './components/Chat';

function App() {
  return (
    <div className="background">
      <div className="shape"></div>
      <div className="shape"></div>
      <div className="shape"></div>

      <div className="App">
        <header className="App-header">
          <h1>🧠 LLaMA RAG Chatbot</h1>
          <Upload />
          <hr style={{ width: '80%', borderColor: '#fff' }} />
          <Chat />
        </header>
      </div>
    </div>
  );
}

export default App;
