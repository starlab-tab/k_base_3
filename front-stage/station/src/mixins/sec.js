import { eld } from "@/mixins/eld.js"
export const archive_editor={
    mixins: [eld],
    props: {
        id: {
            default: undefined
        }
    },
    data: () => ({
        box: {
            name: "paper",
            primary: "#367bf0",
            attach_bar: {
                toolbar: {
                    More: {
                        title: 'More',
                        icon: 'v-md-icon-tip',
                        menus: {
                            mode: 'panel',
                            itemWidth: '56px',
                            rowNum: 5,
                            items: [
                                {
                                    text: 'From md',
                                    action() {
                                        document.getElementById('from_md').click()
                                    }
                                }
                            ],
                        },
                    }
                },
                name: "| More"
            },
            dessert: {
                pf_id: '',
                pf_name: '',
                pf_url: 'https://127.0.0.1',
                author: '',
                date: '',
                title: '',
                content: '',
                visible: true,
                protection: "",
                render: false,
                albums: [],
                chips: [],
            },
            base_dessert: {
                pf_id: '',
                pf_name: '',
                pf_url: 'https://127.0.0.1',
                author: '',
                date: '',
                title: '',
                content: '',
                visible: true,
                protection: "",
                render: false,
                albums: [],
                chips: [],
            },
            all_albums: [],
            als_image_url: "",
            als_image_loading: false,
            rules: {
                required: value => !!value || '',
            },
            required_attrs: ['pf_id', 'pf_name', 'pf_url', 'author', 'title'],
        },
    }),
    created() {
        this.get_detail()
        this.get_albums()
    },
    components: {
        Editor: () => import(`@/components/Global/Editor.vue`)
    },
    methods: {
        get_detail: function() {
            if (!this.id) return
            var numReg = /^[0-9]*$/
            var numReg = new RegExp(numReg)
            if (numReg.test(this.id)) {
                this.$surf.sec.archive.paper.detail(this.id).then(res => {
                    this.box.dessert = {...res.data.data}
                    this.box.base_dessert = {...res.data.data}
                }).catch(err => {
                    this.$router.replace({name: 'SecArchivePaper'})
                })
            }else {
                this.$router.replace({name: 'SecArchivePaper'})
            }
        },
        get_albums: function() {
            this.$surf.sec.archive.album.get(0).then(res => {
                this.box.all_albums = res.data.data.map(x => { return x[0] })
            }).catch(err => {
                
            }).finally(result => {
    
            })
        },
        handle_upload_image: function({data, func}) {
            this.box.als_image_loading = true
            this.$surf.sec.image.upload(data).then(res => {
                func({
                    url: res.data.data,
                    // url: 'http://127.0.0.1:5000' + res.data.data,
                    desc: 'Chappie',
                });
            }).catch(err => {
            }).finally(result => {
                this.box.als_image_loading = false
                this.$shield.down()
            })
        },
        als_image: function(url) {
            this.box.als_image_loading = true
            this.$surf.sec.image.als({url: url}).then(res => {
                this.box.als_image_url = ""
                let result = {
                    text: this.box.dessert.render ? `![Chappie](${res.data.data})` : `<p><img src="${res.data.data}"/></p>`,
                    selected: res.data.data
                }
                this.$refs.Editor.$refs.vmdeditor.insert(function (selected){
                    return result
                })
            }).catch(err => {
            }).finally(result => {
                this.box.als_image_loading = false
                this.$shield.down()
            })
        }
    }
}