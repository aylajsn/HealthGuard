import { useEffect, useState } from "react";

interface CurrentUser {
  authenticated: boolean;
  email?: string;
  name?: string;
}

function App() {
  const [user, setUser] = useState<CurrentUser | null>(null);

  useEffect(() => {
    fetch("http://localhost:8000/auth/me", { credentials: "include" })
      .then((res) => res.json())
      .then(setUser)
      .catch(() => setUser({ authenticated: false }));
  }, []);

  if (!user) {
    return <p>Loading...</p>;
  }

  if (!user.authenticated) {
    return (
      <div style={{ textAlign: "center", marginTop: "100px" }}>
        <h1>HealthGuard</h1>
        <a href="http://localhost:8000/auth/login">Sign in with Google</a>
      </div>
    );
  }

  return (
    <div style={{ textAlign: "center", marginTop: "100px" }}>
      <h1>Welcome, {user.name}</h1>
      <p>Logged in as {user.email}</p>
    </div>
  );
}

export default App;