// input (select + textbox x 2)
Vue.component('v-input', {
  props: ['title', 'description', 'varName', 'searchTermCaption', 'filter'],
  template: `
    <div class="v-form-group">
      <div class="v-title" v-text="title"></div>
      <div class="v-description" v-text="description"></div>

      <div class="row">
        <div class="col-md-4">
          <v-select @changed="updateOp" :value="item.op"></v-select>
        </div>
        <div class="col-md-4">
          <v-textbox @blurred="updateSearchTerm0" :search-term-caption="searchTermCaption" :value="item.searchTerm0"></v-textbox>
        </div>
        <div class="col-md-4" v-if="options.searchTerm1Disabled">
          <v-textbox @blurred="updateSearchTerm1" :search-term-caption="searchTermCaption" :value="item.searchTerm1"></v-textbox>
        </div>
      </div>

      <div class="row v-padding">
        <div class="col-md-12">
          <code>{{item}}</code>
        </div>
      </div>

      <div class="row v-padding">
        <div class="col-md-12">
          <b-button variant="success" size="sm" @click="apply">Apply</b-button>
          <b-button variant="secondary" size="sm" @click="reset">Reset</b-button>
        </div>
      </div>
    </div>
  `,

  data: function() {
    return {
      item: {
        varName: this.varName,
        searchTerm0: this.filter.current.searchTerm[0],
        searchTerm1: this.filter.current.searchTerm[1],
        op: "equals to",
      },
      options: {
        searchTerm1Disabled: false,
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

        // form specific logic
        if (this.item.op == "between") {
          this.options.searchTerm1Disabled = true;
        } else {
          this.options.searchTerm1Disabled = false;
          this.item.searchTerm1 = null;
        }
      },
      deep: true,
    },
  }

})
// end of input
