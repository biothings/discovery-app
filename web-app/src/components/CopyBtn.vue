<template>
    <button v-bind="$attrs" class="btn-copy" @click="copy" :data-clipboard-text="copy_this">
        {{msg}}
    </button>
</template>

<script>
import ClipboardJS from 'clipboard'

export default {
    name: 'CopyBtn',
    props:{
        msg:{
            type: String,
            default: 'share link'
        },
        copy_msg:{
            type: String,
            default: 'Link Copied'
        },
        copy_this:{
            type: String,
            default: ''
        },
    },
    methods:{
        copy:function(){
            this.$swal.fire({
                icon: "success",
                toast: true,
                title: this.copy_msg,
                showConfirmButton: false,
                timer: 1000,
            });
        }
    },
    mounted: function(){
        new ClipboardJS('.btn-copy');
    }
}
</script>