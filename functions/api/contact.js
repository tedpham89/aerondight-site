export async function onRequestPost({ request, env }) {
	try {
		const { name, email, message, website } = await request.json();

		// Validate required fields
		if (
			typeof name !== "string" || !name.trim() ||
			typeof email !== "string" || !email.trim() ||
			typeof message !== "string" || !message.trim()
		) {
			return Response.json(
				{ success: false, error: "All fields are required." },
				{ status: 400 }
			);
		}

		// Basic email validation
		if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim())) {
			return Response.json(
				{ success: false, error: "Please provide a valid email address." },
				{ status: 400 }
			);
		}

		// Honeypot: silently drop if filled
		if (website) {
			return Response.json({ success: true }, { status: 200 });
		}

		const trimmedName = name.trim();
		const trimmedEmail = email.trim();
		const trimmedMessage = message.trim();

		const res = await fetch("https://api.resend.com/emails", {
			method: "POST",
			headers: {
				"Authorization": `Bearer ${env.RESEND_API_KEY}`,
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
				from: env.CONTACT_FROM_EMAIL,
				to: [env.CONTACT_TO_EMAIL],
				reply_to: trimmedEmail,
				subject: `New contact form submission from ${trimmedName}`,
				text: `Name: ${trimmedName}\nEmail: ${trimmedEmail}\n\nMessage:\n${trimmedMessage}`,
				html: `<p><strong>Name:</strong> ${escapeHtml(trimmedName)}</p>
<p><strong>Email:</strong> ${escapeHtml(trimmedEmail)}</p>
<hr>
<p>${escapeHtml(trimmedMessage).replace(/\n/g, "<br>")}</p>`,
			}),
		});

		if (!res.ok) {
			return Response.json(
				{ success: false, error: "Failed to send message. Please try again later." },
				{ status: 502 }
			);
		}

		return Response.json({ success: true }, { status: 200 });
	} catch {
		return Response.json(
			{ success: false, error: "An unexpected error occurred." },
			{ status: 500 }
		);
	}
}

function escapeHtml(str) {
	return str
		.replace(/&/g, "&amp;")
		.replace(/</g, "&lt;")
		.replace(/>/g, "&gt;")
		.replace(/"/g, "&quot;");
}
