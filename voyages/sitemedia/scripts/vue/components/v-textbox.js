// textbox
Vue.component("v-textbox", {
  props: ['searchTermCaption', 'value', 'type'],
  template: `
    <div>
      <b-form-input v-model="textboxValue"
                    :type="type"
                    :placeholder="placeholderValue"
                    @blur.native="emitParent"></b-form-input>
      <div class="v-form-element-caption">{{searchTermCaption}}</div>
      <div>Value: {{ textboxValue }}</div>
    </div>
  `,

  data: function() {
    return {
      textboxValue: '',
      placeholderValue: ''
    }
  },

  methods: {
    emitParent: function() {
      this.$emit('blurred', this.textboxValue);
    }
  },

  watch: {
    value: { // this is the value from props
      handler: function(value) {
        this.textboxValue = value; // textboxValue is the local copy used in the child component
      }
    }
  },

  mounted: function() { // load value initially
    this.textboxValue = this.value;
  }
})
// end of textbox
