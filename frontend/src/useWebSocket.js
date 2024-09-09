const useWebSocket = (url, query) => {
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    const connectToSocket = async () => {
      try {
        const socketToken = await axios.get('/api/auth/soket/');
        if (socketToken) {
          const newSocket = io(url, {
            query: { token: socketToken.data.token, ...query },
          });

          newSocket.on('connect', () => {
            console.log('WebSocket connected');
          });

          newSocket.on('disconnect', () => {
            console.log('WebSocket disconnected');
          });

          setSocket(newSocket);
        }
      } catch (error) {
        console.error('Failed to connect to WebSocket:', error);
      }
    };

    connectToSocket();

    return () => {
      if (socket) {
        socket.disconnect();
      }
    };
  }, [url, query]);

  return socket;
};
