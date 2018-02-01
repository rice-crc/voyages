// v-checkbox
Vue.component('v-checkbox', {
  props: ['title', 'description', 'varName', 'filter', 'isImputed', 'isAdvanced', 'checkboxName'],
  template: `
    <div class="v-form-group">
      <div class="v-title">
        <span>{{title}}</span>
        <span>
          <b-badge
            v-if="isImputed"
            v-b-tooltip.hover title="Imputed variables are calculated by an algorithm and not based on historical records."
            variant="warning"
            class="v-badge-imputed">
            Imputed
          </b-badge>
          <b-badge
            v-if="isAdvanced"
            v-b-tooltip.hover title="Advanced variables are additional parameters that are frequenlty used. They do not change current search behavior."
            variant="danger" class="v-badge-advanced">Advanced</b-badge>
        </span>
      </div>

      <div class="v-description" v-text="description"></div>

      <div class="row">
        <div class="col-md-12">
          <b-form-checkbox id="checkbox1"
                           value="accepted"
                           unchecked-value="not_accepted">
            {{checkboxName}}
          </b-form-checkbox>
        </div>
      </div>

    </div>
  `,

  data: function() {
    return {
      item: {
        // varName: this.varName,
        // searchTerm0: this.filter.current.searchTerm[0],
        // searchTerm1: this.filter.current.searchTerm[1],
        // op: "equals to",
      },
      options: {
        // searchTerm1Disabled: false,
        // searchTermCaption0: null,
        // searchTermCaption1: null,
        // type: "text",
      }
    }
  },

  methods: {
    // form element handlers
    updateSearchTerm0(value) { // handler for variable
      this.item.searchTerm0 = value;
    },
    updateSearchTerm1(value) { // handler for variable
      this.item.searchTerm1 = value;
    },
    updateOp(value) { // handler for variable
      this.item.op = value;
    },

    // form action buttons
    apply() { // simply return the search string to whichever requested for it
      var searchString = JSON.stringify(this.item);
      alert(searchString);
    },
    reset() { // reset data; observers will take care of resetting the controls
      this.item.searchTerm0 = null;
      this.item.searchTerm1 = null;
      this.item.op = "equals to";
    }
  },

  watch: {
    // search object
    item: {
      handler: function(){
        this.$emit('updated', this.item);
      }
    },
    deep: true,
  },

  mounted: function() {
    // debugger;
    // this.options.searchTermCaption0 = this.searchTermCaption;
  }

})
// end of input
