
    new Vue({
        el: "#app",
        delimiters: ["[[", "]]"],
        data: () => {
            return {
                username: "",
                password: "",
                items: [],
                message: "",
                access_token: "",
                refresh_token: "",
                sort_order: "True",
                file_exist: 0
            }
        },
        methods: {
            login: function () {
                axios.post('/token', {
                    username: this.username,
                    password: this.password
                }, {headers: {accept: "application/json", "Content-Type": "application/x-www-form-urlencoded"}})
                    .then((response) => {
                        if (response.status === 200) {
                            this.access_token = response.data.access_token;
                            this.refresh_token = response.data.refresh_token;
                            localStorage.setItem('access_token', this.access_token);
                            localStorage.setItem('refresh_token', this.refresh_token);
                            this.get();
                        } else {
                            this.access_token = "";
                            localStorage.setItem('access_token', "");
                            this.message = response.data.message;
                        }
                    }).catch((e) => {
                    console.log(e.message);
                })
            },
            refresh: function (callback) {
                this.refresh_token = localStorage.getItem("refresh_token");
                if (this.refresh_token) {
                    axios.get('/refresh', {
                        headers: {
                            accept: "application/json",
                            Authorization: "Bearer " + this.refresh_token
                        }
                    }).then((response) => {
                        if (response.status === 200) {
                            this.access_token = response.data.access_token;
                            this.refresh_token = response.data.refresh_token;
                            localStorage.setItem('access_token', this.access_token);
                            localStorage.setItem('refresh_token', this.refresh_token);
                            if (callback) {
                                callback();
                            }
                            ;
                        } else {
                            this.access_token = "";
                            localStorage.setItem('access_token', "");
                            this.message = response.data.message;
                        }
                    }).catch((e) => {
                        console.log(e.message);
                    })
                }
            },
            logout: function () {
                this.access_token = "";
                localStorage.removeItem("access_token");
                window.location.href = '/';
            },
            get: function () {
                this.access_token = localStorage.getItem("access_token");
                if (this.access_token) {
                    this.name('name');
                }
            },
            name: async function (field_name) {
                this.refresh(() => {
                    axios.get('/users/me/', {
                        headers: {
                            accept: "application/json",
                            Authorization: "Bearer " + this.access_token
                        }
                    })
                });
            },
        },
        mounted() {
            this.get();
        }
    })