Vue.component("v-dropdown", {
  props: ['title', 'description', 'options', 'isMultiple', 'clearable'],
  template: `
  <div class="">
    <div class="v-title" v-text="title"></div>
    <div class="v-description" v-text="description"></div>
    <treeselect
      v-model="data.value"
      :multiple="isMultiple"
      :clearable="clearable"
      :close-on-select="true"
      :options="data.options">
    </treeselect>
  </div>
  `,

  components: {
    treeselect: window.VueTreeselect.Treeselect,
  },

  data: function(){
    return {
      data: {
        value: null,
        options: this.options
      }
    }
  },

  methods: {
  },

  watch: {
    // search object
    options: {
      handler: function(){
      },
      deep: true,
    },
  },


});
