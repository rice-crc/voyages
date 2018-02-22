// select2
Vue.component('select2', {
  props: ['options', 'value'],
  template: `
    <select multiple="multiple">
      <slot></slot>
    </select>
  `,
  mounted: function () {
    var vm = this
    $(this.$el)
      // init select2
      .select2({ data: this.options,  multiple: true })
      .val(this.value)
      .trigger('change')
      // emit event on change.
      .on('change', function () {
        vm.$emit('input', $(this).val())
      })
  },
  watch: {
    value: function (value) {
      // update value
      debugger;

      $(this.$el).val(value);

    },
    options: function (options) {
      // update options
      $(this.$el).empty().select2({ data: options })
    }
  },
  destroyed: function () {
    $(this.$el).off().select2('destroy')
  }
})
// end of select2

// v-select2
Vue.component('v-select2', {
    template: `
      <div class="v-form-group">
        <div class="v-title">
          <slot name="title"></slot>
        </div>
        <div class="v-description">
          <slot name="description"></slot>
        </div>

        <div class="row">
          <div class="col-md-12">
            <select2 :options="options" v-model="selected">
              <option disabled >Select one</option>
            </select2>
          </div>
        </div>


        <div class="row v-padding">
          <div class="col-md-12">
            <code>{{selected}}</code>
          </div>
        </div>

        <button @click="clearSelections"> Clear </button>

      </div>
    `,

    data: function() {
      return {
        selected: null,
        options: [
          { id: 1, text: 'Spain / Uruguay' },
          { id: 2, text: 'Portugal / Brazil' },
          { id: 3, text: 'Great Britain' },
          { id: 4, text: 'Netherlands' },
          { id: 5, text: 'U.S.A.' },
          { id: 6, text: 'France' },
          { id: 7, text: 'Denmark / Baltic' },
        ]
      }
    },

    methods: {
      clearSelections: function(){
        this.selected = null;
      }
    }

});
// v-select2
