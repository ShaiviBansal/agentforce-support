import { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { sendMessage } from "../services/api";
import Message from "../components/Message";

interface ChatMessage {
	role: "user" | "agent";
	content: string;
	sources?: string[];
}

const Chat = () => {
	const [messages, setMessages] = useState<ChatMessage[]>([
		{
			role: "agent",
			content: "Hi! I'm your support agent. How can I help you today?",
		},
	]);
	const [input, setInput] = useState("");
	const [loading, setLoading] = useState(false);
	const bottomRef = useRef<HTMLDivElement>(null);
	const navigate = useNavigate();

	// Auto scroll to bottom when new messages arrive
	useEffect(() => {
		bottomRef.current?.scrollIntoView({ behavior: "smooth" });
	}, [messages]);

	const handleSend = async () => {
		if (!input.trim() || loading) return;

		const userMessage = input.trim();
		setInput("");
		setMessages((prev) => [...prev, { role: "user", content: userMessage }]);
		setLoading(true);

		try {
			const result = await sendMessage(userMessage);
			setMessages((prev) => [
				...prev,
				{
					role: "agent",
					content: result.response,
					sources: result.sources,
				},
			]);
		} catch (err) {
			setMessages((prev) => [
				...prev,
				{
					role: "agent",
					content: "Sorry, something went wrong. Please try again.",
				},
			]);
		} finally {
			setLoading(false);
		}
	};

	const handleLogout = () => {
		localStorage.removeItem("token");
		navigate("/");
	};

	return (
		<div
			style={{
				minHeight: "100vh",
				backgroundColor: "#f5f7fa",
				display: "flex",
				flexDirection: "column",
			}}
		>
			{/* Header */}
			<div
				style={{
					backgroundColor: "white",
					padding: "16px 24px",
					boxShadow: "0 1px 4px rgba(0,0,0,0.1)",
					display: "flex",
					justifyContent: "space-between",
					alignItems: "center",
				}}
			>
				<div>
					<h2 style={{ margin: 0, fontSize: "18px", color: "#1a1a1a" }}>
						Support Agent
					</h2>
					<p style={{ margin: 0, fontSize: "12px", color: "#22c55e" }}>
						● Online
					</p>
				</div>
				<button
					onClick={handleLogout}
					style={{
						padding: "8px 16px",
						backgroundColor: "transparent",
						border: "1px solid #ddd",
						borderRadius: "8px",
						cursor: "pointer",
						fontSize: "13px",
						color: "#666",
					}}
				>
					Logout
				</button>
			</div>

			{/* Messages */}
			<div
				style={{
					flex: 1,
					overflowY: "auto",
					padding: "24px",
					maxWidth: "800px",
					width: "100%",
					margin: "0 auto",
					boxSizing: "border-box",
				}}
			>
				{messages.map((msg, index) => (
					<Message
						key={index}
						role={msg.role}
						content={msg.content}
						sources={msg.sources}
					/>
				))}

				{loading && (
					<div
						style={{
							display: "flex",
							justifyContent: "flex-start",
							marginBottom: "16px",
						}}
					>
						<div
							style={{
								padding: "12px 16px",
								borderRadius: "18px 18px 18px 4px",
								backgroundColor: "#f0f0f0",
								color: "#666",
								fontSize: "14px",
							}}
						>
							Thinking...
						</div>
					</div>
				)}
				<div ref={bottomRef} />
			</div>

			{/* Input */}
			<div
				style={{
					backgroundColor: "white",
					padding: "16px 24px",
					boxShadow: "0 -1px 4px rgba(0,0,0,0.1)",
				}}
			>
				<div
					style={{
						maxWidth: "800px",
						margin: "0 auto",
						display: "flex",
						gap: "12px",
					}}
				>
					<input
						type="text"
						value={input}
						onChange={(e) => setInput(e.target.value)}
						onKeyDown={(e) => e.key === "Enter" && handleSend()}
						placeholder="Type your message..."
						disabled={loading}
						style={{
							flex: 1,
							padding: "12px 16px",
							borderRadius: "24px",
							border: "1px solid #ddd",
							fontSize: "14px",
							outline: "none",
							boxSizing: "border-box",
						}}
					/>
					<button
						onClick={handleSend}
						disabled={loading}
						style={{
							padding: "12px 24px",
							backgroundColor: "#0066ff",
							color: "white",
							border: "none",
							borderRadius: "24px",
							fontSize: "14px",
							cursor: loading ? "not-allowed" : "pointer",
							opacity: loading ? 0.7 : 1,
						}}
					>
						Send
					</button>
				</div>
			</div>
		</div>
	);
};

export default Chat;
