import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

const ChatPage = () => {
  const { listingId } = useParams();
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [socket, setSocket] = useState(null);

  // Определяем функцию connectToSocket
  const connectToSocket = async () => {
    try {
      const socketToken = await axios.get('/api/auth/soket/');
      if (socketToken) {
        const newSocket = new WebSocket(`ws://localhost/api/chat/${listingId}/?token=${socketToken.data.token}`);

        newSocket.onmessage = (event) => {
          const messageData = JSON.parse(event.data);
           console.log("Получено сообщение:", messageData);
          setMessages((prevMessages) => [...prevMessages, messageData]);
        };

        newSocket.onopen = () => {
          console.log('WebSocket соединение установлено');
        };

        newSocket.onclose = () => {
          console.log('WebSocket соединение закрыто');
        };

        setSocket(newSocket);
      }
    } catch (error) {
      console.error('Failed to connect to WebSocket:', error);
    }
  };

  useEffect(() => {
    connectToSocket(); // Подключаемся к WebSocket при монтировании компонента

    return () => {
      if (socket) {
        console.log('Закрытие WebSocket соединения');
        socket.close();
      }
    };
  }, [listingId]);

  const sendMessage = () => {
    if (socket && newMessage.trim()) {
      console.log("Отправка сообщения:", newMessage);
      socket.send(JSON.stringify({
        action: 'send_message',
        data: newMessage,
        request_id: listingId,
      }));
      setMessages((prevMessages) => [...prevMessages, { message: newMessage, user: 'You' }]);
      setNewMessage('');
    }
  };

  return (
    <div>
      <div>
        {messages.map((msg, index) => (
          <div key={index}>{msg.user}: {msg.message}</div>
        ))}
      </div>
      <input
        type="text"
        value={newMessage}
        onChange={(e) => setNewMessage(e.target.value)}
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
};

const styles = {
  chatContainer: {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'space-between',
    maxWidth: '600px',
    margin: 'auto',
    height: '80vh',
    border: '1px solid #ccc',
    borderRadius: '8px',
    backgroundColor: '#f9f9f9',
    padding: '20px',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
  },
  messagesContainer: {
    flex: 1,
    overflowY: 'auto',
    paddingRight: '10px',
    marginBottom: '20px',
  },
  message: {
    marginBottom: '10px',
    padding: '8px',
    borderRadius: '8px',
    backgroundColor: '#e0e0e0',
    wordWrap: 'break-word',
  },
  ownMessage: {
    backgroundColor: '#d1e7dd',
    alignSelf: 'flex-end',
  },
  inputContainer: {
    display: 'flex',
    alignItems: 'center',
  },
  messageInput: {
    flex: 1,
    padding: '10px',
    border: '1px solid #ccc',
    borderRadius: '8px',
    marginRight: '10px',
    fontSize: '16px',
  },
  sendButton: {
    padding: '10px 20px',
    border: 'none',
    borderRadius: '8px',
    backgroundColor: '#007bff',
    color: 'white',
    cursor: 'pointer',
  },
};


export default ChatPage;
