import * as server from "server";

const {get, post} = server.router;

server({ port: 3000, public: "./public" }, [
    get("/layout", ctx => {
        return [
            "test"
        ]
    })
]);
