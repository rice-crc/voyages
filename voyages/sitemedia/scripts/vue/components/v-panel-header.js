// v-panel-header
Vue.component('v-panel-header', {
  props: ['title', "description", "modalDisabled"],
  template: `
    <div class="v-panel-header">
      <div class="v-panel-title-container">
        <div class="v-panel-title">
          {{title}}
        </div>
        <div v-if="!modalDisabled" class="v-panel-header-control" >
          <div class="text-center">
            <b-btn variant="outline-info" size="sm" @click="modalShow = !modalShow">
              <i class="fa fa-question-circle-o"></i>
              Help
            </b-btn>
            <b-modal centered v-model="modalShow">
              <div slot="modal-title">
                <div class="v-modal-title">
                  Help Information about {{title}}
                </div>
              </div>
              <slot name="v-modal-content"></slot>
              <div slot="modal-footer">
               <b-btn size="sm" class="float-right" variant="info" @click="modalShow=false">
                 Close
               </b-btn>
             </div>
            </b-modal>
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
      modalTitle: '',
      modalId: '',
      modalShow: false,
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
  },

  mounted: function() { // load value initially
    this.titleValue = this.title;
    this.descriptionValue = this.description;
    this.modalTitle = "Help about " + this.title;
    this.modalId = hyphenate(this.title);
  }

})
// v-panel-header
