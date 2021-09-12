export const albumtable={
    data: () => ({
        box: {
            desserts: [],
            headers: [
                {
                    text: 'Name',
                    value: 'name',
                    sortable: false,
                },
                {
                    text: 'Nums',
                    value: 'nums',
                    filterable: false,
                    align: 'end'
                },
                {
                    text: 'Actions',
                    value: 'actions',
                    align: 'end',
                    custom: true,
                    sortable: false,
                    filterable: false,
                },
            ],
            next_page: 1,
            search: "",
            loading: false,
            last_search: "",
            search_actived: false,
            show_retry: false,
            show_edit_dlg: false,
            show_del_dlg: false,
            edited_index: -1,
            edited_item: {}
        }
    }),
    components: {
        AlbumTable: () => import(`@/components/Global/AlbumTable.vue`),
    }
}