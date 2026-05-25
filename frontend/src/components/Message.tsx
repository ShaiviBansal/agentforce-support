interface MessageProps {
	role: "user" | "agent";
	content: string;
	sources?: string[];
}

const Message = ({ role, content, sources }: MessageProps) => {
	const isUser = role === "user";

	return (
		<div
			style={{
				display: "flex",
				justifyContent: isUser ? "flex-end" : "flex-start",
				marginBottom: "16px",
			}}
		>
			<div
				style={{
					maxWidth: "70%",
					padding: "12px 16px",
					borderRadius: isUser ? "18px 18px 4px 18px" : "18px 18px 18px 4px",
					backgroundColor: isUser ? "#0066ff" : "#f0f0f0",
					color: isUser ? "white" : "#333",
					fontSize: "14px",
					lineHeight: "1.5",
				}}
			>
				<p style={{ margin: 0 }}>{content}</p>

				{sources && sources.length > 0 && (
					<div
						style={{
							marginTop: "8px",
							paddingTop: "8px",
							borderTop: "1px solid rgba(0,0,0,0.1)",
							fontSize: "11px",
							opacity: 0.7,
						}}
					>
						<strong>Sources:</strong>
						{sources.map((source, index) => (
							<p key={index} style={{ margin: "4px 0 0 0" }}>
								• {source.slice(0, 80)}...
							</p>
						))}
					</div>
				)}
			</div>
		</div>
	);
};

export default Message;
