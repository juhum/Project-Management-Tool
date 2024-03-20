<template>
  <Pie v-if="loaded" :data="chartData" />
</template>

<script>
import { Pie } from "vue-chartjs";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import axios from "axios";

ChartJS.register(ArcElement, Tooltip, Legend);
export default {
  name: "PieChart",
  components: { Pie },
  data() {
    return {
      loaded: false,
      chartData: null,
      fields: [],
      currentUser: null,
      fieldColors: {
        "Low": "#FF6384",
        "Medium": "#36A2EB",
        "High": "#FFCE56",
        "New": "#FF6384",
        "Open": "#36A2EB",
        "In Progress": "#FFCE56",
        "Completed": "#4BC0C0",
        "On Hold": "#9966FF",
        "Cancelled": "#FF9F40",
      },
    };
  },
  props: {
    responseData: {
      type: Array,
      required: true,
    },
    showOnlyUserChecker: {
      type: Boolean,
      default: false,
    },
    currentUserId: {
      type: Number,
      required: true,
    },
    dataField: {
      type: Array,
      required: true,
      },
  },
  async mounted() {
    try {
      await this.loadData();
    } catch (error) {
      console.error(error);
    }
  },
  methods: {
    async loadData() {
      try {
        let data = this.responseData;

        if (this.showOnlyUserChecker) {
          data = data.filter((item) => {
            if (item.assigned_to !== undefined) {
              return item.assigned_to === this.currentUserId;
            } else if (
              item.team_members !== undefined &&
              Array.isArray(item.team_members)
            ) {
              return item.team_members.includes(this.currentUserId);
            }
          });
        }

        let dataFields;
        let dataNames;

        if (this.dataField[0].name  !== undefined) {
          dataFields = data.map((item) => item.status);
          this.fields = this.dataField;
          dataNames = dataFields.map((fieldId) =>
          this.getStatusName(fieldId)
        );
        } else if (this.dataField[0].level !== undefined) {
          dataFields = data.map((item) => item.priority_level);
          this.fields = this.dataField;
          dataNames = dataFields.map((fieldId) =>
          this.getPriorityLevelName(fieldId)
          );
        } else {
          throw new Error('Invalid dataField prop value.');
        }
      

        const fieldCounts = this.countFields(dataNames);

        this.chartData = {
          labels: Object.keys(fieldCounts),
          datasets: [
            {
              data: Object.values(fieldCounts),
              backgroundColor: Object.keys(fieldCounts).map(
                (field) => this.fieldColors[field]
              ),
              label: "Number",
            },
          ],
        };

        this.loaded = true;
      } catch (error) {
        console.error(error);
      }
    },
    getStatusName(fieldId) {
      const field = this.fields.find((field) => field.id === fieldId);
      return field ? field.name : "Unknown";
    },
    getPriorityLevelName(priorityLevelId) {
      const level = this.fields.find(
        (level) => level.id === priorityLevelId
      );
      return level ? level.level : "Unknown";
    },
    countFields(fields) {
      return fields.reduce((acc, field) => {
        acc[field] = (acc[field] || 0) + 1;
        return acc;
      }, {});
    },
    async refreshData() {
      try {
        await this.loadData();
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>
