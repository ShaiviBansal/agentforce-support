import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../services/api";

const Login = () => {
	const [username, setUsername] = useState("");
	const [password, setPassword] = useState("");
	const [error, setError] = useState("");
	const [loading, setLoading] = useState(false);
	const navigate = useNavigate();

	const handleLogin = async () => {
		setLoading(true);
		setError("");
		try {
			const token = await login(username, password);
			localStorage.setItem("token", token);
			navigate("/chat");
		} catch (err) {
			setError("Invalid username or password");
		} finally {
			setLoading(false);
		}
	};

	return (
		<div
			style={{
				minHeight: "100vh",
				display: "flex",
				alignItems: "center",
				justifyContent: "center",
				backgroundColor: "#f5f7fa",
			}}
		>
			<div
				style={{
					backgroundColor: "white",
					padding: "40px",
					borderRadius: "12px",
					boxShadow: "0 4px 24px rgba(0,0,0,0.1)",
					width: "100%",
					maxWidth: "400px",
				}}
			>
				<h1 style={{ margin: "0 0 8px 0", fontSize: "24px", color: "#1a1a1a" }}>
					Support Agent
				</h1>
				<p style={{ margin: "0 0 32px 0", color: "#666", fontSize: "14px" }}>
					Sign in to start a support session
				</p>

				<div style={{ marginBottom: "16px" }}>
					<label
						style={{
							display: "block",
							marginBottom: "6px",
							fontSize: "14px",
							color: "#333",
						}}
					>
						Username
					</label>
					<input
						type="text"
						value={username}
						onChange={(e) => setUsername(e.target.value)}
						placeholder="Enter username"
						style={{
							width: "100%",
							padding: "10px 12px",
							borderRadius: "8px",
							border: "1px solid #ddd",
							fontSize: "14px",
							boxSizing: "border-box",
							outline: "none",
						}}
					/>
				</div>

				<div style={{ marginBottom: "24px" }}>
					<label
						style={{
							display: "block",
							marginBottom: "6px",
							fontSize: "14px",
							color: "#333",
						}}
					>
						Password
					</label>
					<input
						type="password"
						value={password}
						onChange={(e) => setPassword(e.target.value)}
						placeholder="Enter password"
						onKeyDown={(e) => e.key === "Enter" && handleLogin()}
						style={{
							width: "100%",
							padding: "10px 12px",
							borderRadius: "8px",
							border: "1px solid #ddd",
							fontSize: "14px",
							boxSizing: "border-box",
							outline: "none",
						}}
					/>
				</div>

				{error && (
					<p style={{ color: "red", fontSize: "13px", marginBottom: "16px" }}>
						{error}
					</p>
				)}

				<button
					onClick={handleLogin}
					disabled={loading}
					style={{
						width: "100%",
						padding: "12px",
						backgroundColor: "#0066ff",
						color: "white",
						border: "none",
						borderRadius: "8px",
						fontSize: "15px",
						cursor: loading ? "not-allowed" : "pointer",
						opacity: loading ? 0.7 : 1,
					}}
				>
					{loading ? "Signing in..." : "Sign In"}
				</button>
			</div>
		</div>
	);
};

export default Login;
