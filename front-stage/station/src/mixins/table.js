export const table={
    data: () => ({
        box: {
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
        this.action({data: this.box.next_page, type: "get"})
    },
    components: {
        DataTable: () => import(`@/components/Global/DataTable.vue`),
    }
}