// v-submenu
Vue.component('v-submenu', {
  props: ['title', "isAdvanced"],
  template: `
    <v-panel :title="title" :isAdvanced="isAdvanced"></v-panel>
  `,

  data: function() {
    return {
      titleValue: '',
      isAdvancedValue: '',
      idValue: null,
      count: 25,
    }
  },

  methods: {
    // calculate() {
    //   debugger;
    // },
    // increment() {
    //   this.count = this.count + 1;
    //   this.$emit('applied', this.count);
    // },
    // announce() {
    //   this.$emit('announced');
    // },
    // reset() {
    //   this.$emit('reset');
    // }
  },
  watch: {
    // count: {
    //   handler: function(){
    //     this.$emit('applied', this.count);
    //   }
    // }
  },

  mounted: function() { // load value initially
    this.titleValue = this.title;
    this.isAdvancedValue = this.isAdvanced;
    this.idValue = hyphenate(this.title);
  }

})
// v-submenu
