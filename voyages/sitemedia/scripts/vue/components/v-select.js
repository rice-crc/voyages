// select
Vue.component('v-select', {
  props: ["value"],
  template: `
    <div>
      <b-form-select v-model="selected" :options="options" @change="emitParent"></b-form-select>
      <!--<div>Selected: <strong>{{selected}}</strong></div>-->
    </div>
  `,
  data: function() {
    return {
      selected: "equals to",
      options: ['is less than',  'equals to', 'is more than', 'is between'],
    }
  },
  methods: {
    emitParent: function(value) {
      this.$emit('changed', value);
    }
  },
  watch: {
    value: {
      handler: function(value) {
        this.selected = this.value;
      }
    }
  },
  created: function() {
    this.selected = this.value;
  }

})
// end of select
