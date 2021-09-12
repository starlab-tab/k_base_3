export const table={
    data: () => ({
        box: {
            name: "",
            desserts: [],
            headers: [],
            next_page: 1,
            search: "",
            loading: false,
            last_search: "",
            search_actived: false,
            show_retry: false,
        }
    }),
    created() {
        this.action({data: {page: this.box.next_page, name: this.name}, type: "get"})
    },
    components: {
        AlbumTable: () => import(`@/components/Global/AlbumTable.vue`)
    },
}