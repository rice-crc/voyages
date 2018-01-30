// select
Vue.component('v-select', {
  props: ['value'],
  template: `
    <div>
      <b-form-select v-model="selected" :options="options" @change="emitParent"></b-form-select>
      <div>Selected: <strong>{{selected}}</strong></div>
    </div>
  `,
  data: function() {
    return {
      selected: "equals to",
      options: ['is less than',  'equals to', 'is more than', 'between'],
    }
  },
  methods: {
    emitParent: function(value) {
      debugger;
      this.$emit('changed', value);
    }
  },
  watch: {
    value: {
      handler: function(value) {
        this.selected = value;
      }
    }
  }
})
// end of select
