// v-panel
Vue.component('v-panel', {
  props: ['title', "isAdvanced"],
  template: `
    <li v-if="isAdvancedValue" class="dropdown-item dropdown-item-li search-dropdown-item" :data-submenu-id="idValue">
        <div class="dropdown-menu-title">
          <div class="dropdown-menu-title-text">
            {{titleValue}}
          </div>
          <div class="dropdown-menu-title-count">
            <b-badge variant="danger">{{count}}</b-badge>
          </div>
        </div>
        <div :id="idValue" class="search-submenu popover">
            <div class="popover-content">
              <slot :count="count" name="v-panel-header"></slot>
              <slot name="v-panel-content"></slot>
              <slot name="v-panel-control"></slot>
              <div class="margin-v">
              <b-button variant="info" size="sm" @click="announce">
              Apply
              </b-button>
              <b-button variant="outline-secondary" size="sm" @click="reset">
              Reset
              </b-button>
              </div>
            </div>
        </div>
    </li>
  `,

  data: function() {
    return {
      titleValue: '',
      isAdvancedValue: '',
      idValue: null,
      count: 0,
    }
  },

  methods: {
    increment: function() {
      this.count = this.count + 1;
      this.$emit('applied', this.count);
    },
    announce: function() {
      debugger;
      this.$emit('announced');
    },
    reset: function() {
      this.$emit('reset');
    }
  },
  watch: {
    count: {
      handler: function(){
        debugger;
        this.$emit('applied', this.count);
      }
    }
  },

  mounted: function() { // load value initially
    this.titleValue = this.title;
    this.isAdvancedValue = this.isAdvanced;
    this.idValue = hyphenate(this.title);
  }

})
// v-panel

// v-panel-header
Vue.component('v-panel-header', {
  props: ['title', "description", "count"],
  template: `
    <div class="v-panel-header">
      <div class="v-panel-title-container">
        <div class="v-panel-title">
        {{title}}
        </div>
        <div class="v-panel-counter">
          <div class="text-center">
          <!--
            <b-button variant="info" size="sm">
              Parameters Applied <b-badge variant="light">{{count}}</b-badge>
            </b-button>
          -->
          <b-button variant="outline-info" size="sm">
            <i class="fa fa-question-circle-o"></i>
            Help
          </b-button>
          </div>
        </div>
      </div>
      <div class="v-panel-description" v-text="description"></div>

    </div>
  `,

  data: function() {
    return {
      titleValue: '',
      descriptionValue: '',
      countValue: null,
    }
  },

  methods: {
    emitParent: function() {
      this.$emit('blurred', this.textboxValue);
    }
  },

  watch: {
    title: { // this is the value from props
      handler: function(value) {
        this.titleValue = value; // titleValue is the local copy used in the child component
      }
    },
    description: {
      handler: function(value) {
        this.descriptionValue = value; // descriptionValue is the local copy used in the child component
      }
    },
    count: {
      handler: function(value) {
        this.countValue = value; // countValue is the local copy used in the child component
      }
    },


  },

  mounted: function() { // load value initially
    this.titleValue = this.title;
    this.descriptionValue = this.description;
    this.countValue = this.count;
  }

})
// v-panel-header
