import React, { useState, useEffect } from "react";
import { auth } from "./firebase";
import { onAuthStateChanged, signOut } from "firebase/auth";
import { 
  Box, 
  CircularProgress,
  IconButton,
  Snackbar,
  Alert,
  Paper
} from "@mui/material";
import LogoutIcon from "@mui/icons-material/Logout";
import SignInForm from "./components/SignInForm";
import ChatInterface from "./components/ChatInterface";

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, user => {
      setUser(user);
      setLoading(false);
    }, error => {
      setError("Failed to check authentication state");
      setLoading(false);
    });

    return () => unsubscribe();
  }, []);

  const handleLogout = async () => {
    try {
      await signOut(auth);
    } catch (error) {
      setError("Logout failed. Please try again.");
      console.error("Logout error:", error);
    }
  };

  const handleErrorClose = () => {
    setError(null);
  };

  if (loading) {
    return (
      <Box 
        display="flex" 
        justifyContent="center" 
        alignItems="center" 
        minHeight="100vh"
      >
        <CircularProgress size={60} thickness={4} />
      </Box>
    );
  }

  return (
    <Paper 
      sx={{
        minHeight: '100vh',
        bgcolor: 'background.default'
      }}
    >
      <Box sx={{ position: 'relative', p: 2 }}>
        {user && (
          <IconButton
            onClick={handleLogout}
            sx={{
              position: 'fixed',
              right: 24,
              top: 24,
              zIndex: 1000,
              bgcolor: 'error.main',
              '&:hover': { bgcolor: 'error.dark' }
            }}
            aria-label="Logout"
          >
            <LogoutIcon sx={{ color: 'common.white' }} />
          </IconButton>
        )}
        
        {user ? (
          <ChatInterface />
        ) : (
          <Box
            display="flex"
            justifyContent="center"
            alignItems="center"
            minHeight="90vh"
          >
            <SignInForm />
          </Box>
        )}
      </Box>

      <Snackbar
        open={!!error}
        autoHideDuration={6000}
        onClose={handleErrorClose}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert 
          severity="error" 
          variant="filled"
          onClose={handleErrorClose}
          sx={{ width: '100%' }}
        >
          {error}
        </Alert>
      </Snackbar>
    </Paper>
  );
}

export default App;
