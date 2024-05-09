import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import FarmDataProvider from './service/farm_data_context';
import ImageProvider from './service/image_context';
import ChatProvider from './service/chat_context';

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <React.StrictMode>
    <FarmDataProvider>
      <ImageProvider>
        <ChatProvider>
        <App />
        </ChatProvider>
      </ImageProvider>
    </FarmDataProvider>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
