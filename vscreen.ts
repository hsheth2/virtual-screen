import * as server from "server";

const {get, post} = server.router;

const screens = {
	left: {
		used: false
	},
	right: {
		used: true,
		name: "VIRTUAL_0"
	},
	up: {
		used: false
	},
	down: {
		used: false
	}
};

server({port: 3000, security: {csrf: false}}, [
	get("/layout", ctx => {
		return screens;
	}),
	post("/addScreen", ctx => {
		const direction = ctx.body;
	})
]);
