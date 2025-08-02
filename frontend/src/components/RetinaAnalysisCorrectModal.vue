<template>
    <div tabindex="-1"
    class="flex align-items-center justify-cneter overflow-y-auto overflow-x-hidden fixed top-0 right-0 left-0 z-50 justify-center items-center w-full md:inset-0 h-[calc(100%-1rem)] max-h-full">
        <div class="modal-background"></div>
        <div class="relative p-4 w-full max-w-2xl max-h-full">
            <!-- Modal content -->
            <div class="relative bg-white rounded-lg shadow dark:bg-gray-700">
                <!-- Modal header -->
                <div class="flex items-center justify-between p-4 md:p-5 border-b rounded-t dark:border-gray-600">
                    <div class="text-xl font-semibold text-gray-900 dark:text-white">
                        Форма исправления результатов анализа
                    </div>
                    <button type="button" @click="close();"
                        class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center dark:hover:bg-gray-600 dark:hover:text-white"
                        data-modal-hide="default-modal">
                        <svg class="w-3 h-3" xmlns="http://www.w3.org/2000/svg" fill="none"
                            viewBox="0 0 14 14">
                            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6" />
                        </svg>
                        <span class="sr-only">Закрыть окно</span>
                    </button>
                </div>
                <!-- Modal body -->
                <div class="p-4 md:p-5 space-y-4">
                    <template v-if="crops.length > 0 && cropResults.length > 0">
                        <!--Сверху картинка снизу метки-->
                        <div class="flex items-center justify-center">
                            <img style="height: 200px; object-fit: contain;" :src="crops[selectCropIndex].get_image" alt="">
                        </div>
                        <div class="flex flex-row" v-if="crops.length > 1">
                            <div v-for="(crop, index) in crops" class="inline-flex mr-3 cursor-pointer">
                                <img class="retina-crop__cover" @click="selectCropIndex=index" :src="crop.get_image"/>
                            </div>
                        </div>
                        <div style="max-height: 300px; overflow-y: scroll;">
                            <div v-for="labelGroup in labelGroups" class="mb-4" :key="labelGroup.id">
                                <span class=" flex text-blue-600 mb-2">{{ labelGroup.name }}</span>
                                <div class="flex flex-row items-center mb-1" v-for="labelMark in getLabelsByGroup(labelGroup.id)" :key="labelMark.id">
                                    <RoundCheckbox class="mr-2 ml-2" v-model="cropResults[selectCropIndex][labelMark.id]" :key="labelMark.id"></RoundCheckbox>
                                    <span :key="labelMark.id">{{ labelMark.name }}</span>
                                </div>
                            </div>
                        </div>
                    </template>
                    <template v-else>
                        Нет выбранных сегментов!
                    </template>
                </div>
                <!-- Modal footer -->
                <div class="flex items-center justify-end p-4 md:p-5 border-t border-gray-200 rounded-b dark:border-gray-600">
                    <button type="button"
                    class="flex flex-row text-blue-800 bg-blue-100 hover:bg-blue-200 focus:outline-none text-sm px-5 py-2 text-center rounded-sm mr-4" @click="correctResults()">Изменить результаты</button>
                    <button dtype="button"
                    class="flex flex-row text-gray-800 bg-gray-200 hover:bg-gray-300 focus:outline-none text-sm px-5 py-2 text-center rounded-sm" @click="close()">Отмена</button>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import axios from "axios";

import RoundCheckbox from "./RoundCheckbox.vue";

export default {
    name: 'RetinaAnlysisCorrectModal',
    props: {
        taskId: { type: String },
        labelGroups: { type: Object },
        labelMarks: { type: Object },
        crops: {type: Array}
    },
    data() {
        return {
            /**
             * Выбранный сегмент для анализа
             */
            selectCropIndex: 0,
            
            /**
             * Исправленные результаты анализа
             */
            cropResults: [],

            /**
             * Исходные результаты анализа
             */
            analysisResults: {},

            /**
             * Результаты от сервера
             */
            correctedResults: {
                isCorrected: false,
                labels: [],
            }
        }
    },
    mounted() {
        //this.getLabelTypes();
        //this.getAvailableLabels();
    },
    computed: {

    },
    methods: {
        /**
         * Получение групп ОКТ маркеров
         */
        getLabelTypes() {
            axios.get("/api/v1/retinadeepai/constants/label-groups/")
            .then((response) => {
                this.labelGroups = response.data;
            })
            .catch((error) => {
                console.log(error);
            });
        },
        /**
         * Получение ОКТ маркеров
         */
        getAvailableLabels() {
            axios.get("/api/v1/retinadeepai/constants/label-marks/")
            .then((response) => {
                this.labelMarks = response.data;
            })
            .catch((error) => {
                console.log(error);
            });
        },
        close() {
            this.selectCropIndex = 0;
            this.cropResults = [];
            this.analysisResults = {};
            this.correctedResults.isCorrected = false;
            this.correctedResults.labels = [];
            this.$emit("close");
        },
        /**
         * Получение маркеров по ID группе
         */
        getLabelsByGroup(groupId) {
            let ttt =  this.labelMarks.filter(lm => lm.group_id == groupId);
            return ttt;
        },
        initCropResults() {
            this.cropResults = [];
            this.correctedResults.isCorrected = false;
            this.correctedResults.labels = [];
            for(let i=0;i<this.crops.length;i++) {
                let cropResult = {};
                let cropID = this.crops[i].id;
                for(let j=0;j<this.labelMarks.length;j++) {
                    cropResult[this.labelMarks[j].id] = false;
                    let labelID = this.labelMarks[j].id;
                    if(this.analysisResults[cropID].includes(labelID)) {
                      cropResult[this.labelMarks[j].id] = true;
                    }
                }
                this.cropResults.push(cropResult) 
            }
        },
        correctResults() {
            console.log(this.labelGroups);
            let task_id = this.taskId;
            let correctRes = [];

            for(let i=0;i<this.cropResults.length;i++) {
                let cropResultIter = {
                    'crop_id': this.crops[i].id,
                    'labels': []
                }
                // перебор значений
                for (let label_id of Object.keys(this.cropResults[i])) {
                    if(this.cropResults[i][label_id] == true) {
                        cropResultIter['labels'].push(label_id);
                    }
                }
                correctRes.push(cropResultIter);
            }

            let request_data = {
                'data': correctRes
            };

            axios({
                method: "post",
                url: `/api/v1/retinadeepai/analysis/tasks/correct/${task_id}/`,
                data: request_data,
            })
            .then(response => {
                this.selectCropIndex = 0;
                this.cropResults = [];
                this.analysisResults = {};
                this.correctedResults.isCorrected = response.data.task_analysis.is_corrected;
                this.correctedResults.labels = response.data.corrected;
                this.$emit("correct");
            })
            .catch(error => {
                console.log(error);
            });
        }
    },
    components: {
        RoundCheckbox,
    }
}
</script>

<style scoped>
.modal-background {
  background-color: #9f9e9ecc;
  bottom: 0;
  left: 0;
  position: absolute;
  right: 0;
  top: 0;
}

.retina-crop__cover {
  width: 54px;
  min-width: 54px;
  height: 32px;
  min-height: 32px;
  object-fit: cover;
}

</style>