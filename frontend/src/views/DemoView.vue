<template>
  <main>
    <div class="mx-auto p-4">
      <div class="demo">
        <!--Основная форма-->
        <div class="retina-app">
          <RetinaAnalysisCorrectModal :class="{
            hidden:
              !taskAnalisis.isCorrected ||
              taskAnalisis.status != STATUS_SUCCESS,
          }" ref="correctModal" @close="correctModalClose()" @correct="correctUpdateResults()" :label-marks="labelMarks" :label-groups="labelGroups"
            :task-id="taskAnalisis.id.model" :crops="taskAnalisis.crops"></RetinaAnalysisCorrectModal>
          <ImageModalWindow :show-modal="imageModalView.isActive" :image-src="imageModalView.src"
            @close="closeImageModal()"></ImageModalWindow>
          <div class="retina-app__sidebar">
            <aside class="retina-menu p-5">
              <div class="retina-menu__item mb-5">
                <p class="uppercase tracking-wider mb-2" :class="{
                  'text-blue-700 font-medium': stepActive == this.STEP_UPLOAD,
                }">
                  1. Выбор изображения
                </p>
                <div class="flex flex-col">
                  <div class="flex justify-between">
                    <button
                      class="flex flex-row text-blue-800 bg-blue-100 hover:bg-blue-200 focus:outline-none text-sm px-5 py-2 text-center rounded-sm disabled:bg-blue-50 disabled:text-blue-800 disabled:cursor-not-allowed"
                      @click="chooseFile" :disabled="appStatus == STATUS_PROGRESS">
                      <template v-if="taskUpload.status == STATUS_PROGRESS">
                        <span>
                          <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-blue-800" xmlns="http://www.w3.org/2000/svg"
                            fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4">
                            </circle>
                            <path class="opacity-75" fill="currentColor"
                              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                            </path>
                          </svg>
                        </span>
                        <span>Идет загрузка...</span>
                      </template>
                      <template v-else>
                        <span>Загрузить</span>
                      </template>
                    </button>
                    <input accept="image/png,.png,image/jpeg,.jpeg,.jpg,application/pdf,.jfif,.tiff" type="file"
                      tabindex="-1" style="display: none" id="fileUpload" @change="uploadImage('fileUpload')" />
                    <button v-if="examples.length > 0"
                      class="text-blue-800 bg-blue-100 hover:bg-blue-200 focus:outline-none text-sm px-5 py-2 text-center rounded-sm"
                      :disabled="appStatus == STATUS_PROGRESS">
                      Примеры
                    </button>
                  </div>
                  <div v-if="
                    taskUpload.status == STATUS_SUCCESS ||
                    taskUpload.status == STATUS_ERROR
                  ">
                    <div class="text-center mt-1" v-bind:class="{
                      'text-green-700': taskUpload.status == STATUS_SUCCESS,
                      'text-red-700': taskUpload.status == STATUS_ERROR,
                    }">
                      {{ taskUpload.statusText }}
                    </div>
                  </div>
                </div>
              </div>
              <div class="retina-menu__item mb-5">
                <div class="flex items-center mb-2">
                  <p class="uppercase tracking-wider" :class="{
                    'text-blue-700 font-medium':
                      stepActive == this.STEP_DETECTION,
                  }">
                    2. Распознавание сегментов
                  </p>
                  <div class="flex items-center" style="margin-left: auto" v-if="taskDetection.crops.length > 0">
                    <span @click="
                      taskDetection.viewMode = DETECTION_VIEW_MODE_BOXES
                      " :class="{
                        'text-blue-600':
                          taskDetection.viewMode == DETECTION_VIEW_MODE_BOXES,
                        'text-gray-600':
                          taskDetection.viewMode == DETECTION_VIEW_MODE_ORIG,
                      }" class="ml-2 cursor-pointer hover:text-blue-500" title="Показать разметку детекции">
                      <IconSquareStack />
                    </span>
                    <span @click="taskDetection.viewMode = DETECTION_VIEW_MODE_ORIG"
                      class="ml-2 cursor-pointer hover:text-blue-500" :class="{
                        'text-blue-600':
                          taskDetection.viewMode == DETECTION_VIEW_MODE_ORIG,
                        'text-gray-600':
                          taskDetection.viewMode == DETECTION_VIEW_MODE_BOXES,
                      }" title="Показать исходное изображение">
                      <IconImage />
                    </span>
                  </div>
                </div>
                <div class="flex flex-col" v-if="stepActive > STEP_UPLOAD">
                  <div class="flex flex-row mb-2">
                    <span class="inline-flex">
                      <CheckboxRadio v-model="taskDetection.isOBB" :value="taskDetection.isOBB"
                        :disabled="taskDetection.status == STATUS_PROGRESS"></CheckboxRadio>
                    </span>
                    <span class="ml-4">Учитывать повороты при распознавании</span>
                  </div>
                  <div class="flex justify-between">
                    <button
                      class="flex flex-row text-blue-800 bg-blue-100 hover:bg-blue-200 focus:outline-none text-sm px-5 py-2 text-center rounded-sm disabled:bg-blue-50 disabled:text-blue-800 disabled:cursor-not-allowed"
                      :disabled="appStatus == STATUS_PROGRESS" @click="detectionFile">
                      <template v-if="taskDetection.status == STATUS_PROGRESS">
                        <span>
                          <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-blue-800" xmlns="http://www.w3.org/2000/svg"
                            fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4">
                            </circle>
                            <path class="opacity-75" fill="currentColor"
                              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                            </path>
                          </svg>
                        </span>
                        <span>Идет распознавание...</span>
                      </template>
                      <template v-else>
                        <span>Найти объекты</span>
                      </template>
                    </button>
                  </div>
                  <div v-if="
                    taskDetection.status == STATUS_SUCCESS ||
                    taskDetection.status == STATUS_ERROR ||
                    taskDetection.status == STATUS_PROGRESS
                  ">
                    <div class="text-center mt-1" v-bind:class="{
                      'text-green-700':
                        taskDetection.status == STATUS_SUCCESS,
                      'text-red-700': taskDetection.status == STATUS_ERROR,
                    }">
                      {{ taskDetection.statusText }}
                    </div>
                    <div class="mt-4">
                      <div class="mb-4 retina-crop" v-for="crop in taskDetection.crops" :key="crop.id">
                        <div class="flex flex-row items-center">
                          <div class="flex mr-3 cursor-pointer" title="Открыть оригинал изображения в новой вкладке"
                            @click="openImageModal(crop.get_image)">
                            <img class="retina-crop__cover" :src="crop.get_thumbnail" />
                          </div>
                          <span class="mr-4">Горизонтальная проекция сетчатки ({{
                            (crop.confidence * 100).toFixed(2)
                          }}%)</span>
                          <span class="inline-flex" style="margin-left: auto">
                            <CheckboxRadio :key="crop.id" v-model="crop.select"
                              :disabled="taskDetection.crops.length == 0" :value="crop.select"></CheckboxRadio>
                          </span>
                        </div>
                        <div>
                          <div v-if="!crop.select" class="retina-crop__status text-red-700">
                            Не учитывать изображение при анализе
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="retina-menu__item mb-5">
                <p class="uppercase tracking-wider mb-2" :class="{
                  'text-blue-700 font-medium':
                    stepActive == this.STEP_ANALYSIS
                }">
                  3. Анализ изображения
                </p>
                <div class="flex flex-col" v-if="stepActive > STEP_DETECTION">
                  <div class="flex justify-between">
                    <button
                      class="flex flex-row text-blue-800 bg-blue-100 hover:bg-blue-200 focus:outline-none text-sm px-5 py-2 text-center rounded-sm mr-4"
                      :disabled="appStatus == STATUS_PROGRESS" @click="analysisFile()">
                      <template v-if="taskAnalisis.status == STATUS_PROGRESS">
                        <span>
                          <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-blue-800" xmlns="http://www.w3.org/2000/svg"
                            fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4">
                            </circle>
                            <path class="opacity-75" fill="currentColor"
                              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                            </path>
                          </svg>
                        </span>
                        <span>Идет анализ...</span>
                      </template>
                      <template v-else>
                        <span>Анализ изображения</span>
                      </template>
                    </button>
                    <button
                      class="flex flex-row items-center text-amber-800 bg-amber-100 hover:bg-amber-200 focus:outline-none text-sm px-5 py-2 text-center rounded-sm"
                      v-if="taskAnalisis.status == STATUS_SUCCESS" @click="correctModalOpen">
                      <span>
                        <svg class="mr-2 h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                          stroke-width="1.5" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round"
                            d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L6.832 19.82a4.5 4.5 0 0 1-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 0 1 1.13-1.897L16.863 4.487Zm0 0L19.5 7.125" />
                        </svg>
                      </span>
                      <span>Уточнить результат</span>
                    </button>
                  </div>
                  <div v-if="
                    taskAnalisis.status == STATUS_SUCCESS ||
                    taskAnalisis.status == STATUS_ERROR ||
                    taskAnalisis.status == STATUS_PROGRESS
                  ">
                    <div class="text-center mt-1" v-bind:class="{
                      'text-green-700': taskAnalisis.status == STATUS_SUCCESS,
                      'text-red-700': taskAnalisis.status == STATUS_ERROR,
                    }">
                      {{ taskAnalisis.statusText }}
                    </div>
                  </div>
                </div>
              </div>
            </aside>
          </div>
          <div class="retina-app__body">
            <div class="retina-image-wrapper max-w-[950px]" style="margin: 0 auto;">
              <div class="retina-image-container">
                <img v-if="taskUpload.status == STATUS_SUCCESS" class="retina-image-cover" v-bind:src="coverMainURL"
                  alt="" style="max-height: 420px; object-fit: contain" />
                <div v-else></div>
              </div>
            </div>
            <div class="retina-results-wrapper">
              <div class="flex flex-col max-w-[950px]" style="margin: 0 auto; width: 100%">
                <template v-if="
                  taskAnalisis.status == STATUS_SUCCESS &&
                  taskAnalisis.resultsFormat.length == 0
                ">
                  <div class="flex flex-row mb-4 p-4 bg-orange-200 text-orange-700 rounded">
                    <span class="inline-flex mr-4 items-center">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round"
                          d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />
                      </svg>
                    </span>
                    <span>Не найдены метки, на которых обучалась модель для
                      распознавания. Вы можете загрузить новое изображение или
                      заполнить описание вручную и выгрузить отчет.</span>
                  </div>
                </template>
                <template v-if="
                  taskAnalisis.status == STATUS_SUCCESS &&
                  taskAnalisis.results.length > 0 && !taskAnalisis.correctedResults.isCorrect
                ">
                  <div class="mt-1 mb-3 flex flex-col settings-block">
                    <div class="flex justify-between unselectable">
                      <div class="mr-4">
                        <span>Отображать результаты с точностью выше: </span><span class="settings-block__menu" @click="
                          thresholdFilter.isExpand = !thresholdFilter.isExpand
                          ">{{ (thresholdFilter.value * 100).toFixed(2) }}%</span>
                      </div>
                      <span class="cursor-pointer settings-block__menu settings-block__menu_expand" @click="
                        thresholdFilter.isExpand = !thresholdFilter.isExpand
                        ">
                        <IconPencilSquare></IconPencilSquare>
                      </span>
                    </div>
                    <div v-if="thresholdFilter.isExpand" class="flex justify-between mt-2">
                      <input type="text" v-model="thresholdFilter.tempValue" class="mr-4 bg-gray-50 border border-gray-300 px-5 text-center w-[100px]" />
                      <button @click="
                        thresholdFilter.value =
                        thresholdFilter.tempValue < 50
                          ? 0.5
                          : thresholdFilter.tempValue > 100
                            ? 1
                            : thresholdFilter.tempValue / 100.0;
                      thresholdFilter.isExpand = false;
                      updateThreasholdValue();
                      " class="text-blue-800 bg-blue-100 hover:bg-blue-200 focus:outline-none text-sm px-5 py-2 text-center rounded-sm">
                        Изменить
                      </button>
                    </div>
                  </div>
                  <div class="content-expander mb-4 select-none" :class="{
                    'content-expander_expand': groupResults.isExpand,
                  }" v-for="groupResults in taskAnalisis.resultsFormat">
                    <div class="content-expander__header" @click="groupResults.isExpand = !groupResults.isExpand">
                      <div class="content-expander__title">
                        <span class="content-expander__icon">
                          <IconChevronRight class="w-4" :class="{ 'rotate-90': groupResults.isExpand }">
                          </IconChevronRight>
                        </span>
                        <span>{{ groupResults.name }}</span>
                      </div>
                    </div>
                    <transition name="expand" @enter="enter" @after-enter="afterEnter" @leave="leave">
                      <div class="content-expander__body" v-show="groupResults.isExpand">
                        <div class="content-expander__actions">
                          <div class="expander-action">
                            <span class="expander-action__title mr-3 text-xs">Сортировать</span>
                            <span title="Сортировать по точности" @click="
                              groupResults.sortState =
                              groupResults.sortState == SORT_STATE_BOOK
                                ? SORT_STATE_SCORE_ASC
                                : groupResults.sortState ==
                                  SORT_STATE_SCORE_DESC
                                  ? SORT_STATE_SCORE_ASC
                                  : SORT_STATE_SCORE_DESC
                              " class="expander-action__icon mr-1" :class="{
                                'expander-action__icon_selected':
                                  groupResults.sortState != SORT_STATE_BOOK,
                              }">
                              <IconBarsArrowUp :class="{
                                'rotate-180':
                                  groupResults.sortState ==
                                  SORT_STATE_SCORE_ASC,
                              }">
                              </IconBarsArrowUp>
                            </span>
                            <span title="Сортировать по справочнику" @click="groupResults.sortState = SORT_STATE_BOOK"
                              class="expander-action__icon" :class="{
                                'expander-action__icon_selected':
                                  groupResults.sortState == SORT_STATE_BOOK,
                              }">
                              <IconNumberedList></IconNumberedList>
                            </span>
                          </div>
                        </div>
                        <div class="content-expander__table expander-table">
                          <div v-for="labelGroup in sortLabelMarks(
                            groupResults.labels,
                            groupResults.sortState
                          )" class="expander-table-row mb-3">
                            <div class="expander-table-row__header">
                              <RoundCheckbox v-model="labelGroup.isSelect" class="mr-2"
                                @change="updateReportTextByMark()"></RoundCheckbox>
                              <span class="expander-table-row__title mr-4 unselectable" :class="{
                                'expander-table-row__expand':
                                  labelGroup.cropsVisible,
                              }" style="font-size: 15px" @click="
                                  labelGroup.cropsVisible =
                                  !labelGroup.cropsVisible
                                  ">{{ labelGroup.name }}</span>
                              <span style="
                                  margin-left: auto;
                                  font-weight: 500;
                                  font-size: 14px;
                                ">{{
                                  (labelGroup.accuracy * 100).toFixed(2)
                                }}%</span>
                            </div>
                            <div class="expander-table-row__body ml-6 mt-1 is-flex" v-if="labelGroup.cropsVisible">
                              <img v-for="labelCrop in labelGroup.crops" style="
                                  height: 22px;
                                  width: 40px;
                                  object-fit: cover;
                                " class="mr-2 cursor-pointer" :src="labelCrop.thumbnailURL" @click="openImageModal(labelCrop.imageURL)" alt="" />
                            </div>
                          </div>
                        </div>
                      </div>
                    </transition>
                  </div>
                </template>
                <template v-if="taskAnalisis.status == STATUS_SUCCESS">
                  <div class="flex flex-col mb-[4rem]">
                    <div class="text-sm uppercase tracking-wider text-blue-700 font-medium mb-1">
                      <span>Описание файла:</span>
                      <span v-if="taskAnalisis.correctedResults.isCorrect" class="ml">(скорректированы)</span>
                    </div>
                    <textarea style="min-height: 130px; font-size: 16px; color: #494949"
                      class="block p-2.5 w-full text-sm outline-none bg-gray-50 rounded-lg border border-gray-200 focus:ring-blue-600"
                      placeholder="Добавьте описание изображения" rows="8" v-model="taskReport.reportText"></textarea>
                    <button
                      class="flex flex-row justify-center text-blue-800 bg-blue-100 hover:bg-blue-200 focus:outline-none text-sm px-5 py-2 text-center rounded-sm mt-3"
                      :disabled="appStatus == STATUS_PROGRESS" @click.stop="generateReport">
                      <template v-if="taskReport.status == STATUS_PROGRESS">
                        <span>
                          <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-blue-800" xmlns="http://www.w3.org/2000/svg"
                            fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4">
                            </circle>
                            <path class="opacity-75" fill="currentColor"
                              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                            </path>
                          </svg>
                        </span>
                        <span>Идет генерация отчета...</span>
                      </template>
                      <template v-else>
                        <span>Выгрузить отчет</span>
                      </template>
                    </button>
                  </div>
                </template>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
import axios from "axios";

import CheckboxRadio from "@/components/CheckboxRadio.vue";
import ImageModalWindow from "@/components/ImageModalWindow.vue";
import IconSquareStack from "@/components/icons/IconSquareStack.vue";
import IconImage from "@/components/icons/IconImage.vue";
import IconDocumentation from "@/components/icons/IconDocumentation.vue";
import IconNumberedList from "@/components/icons/IconNumberedList.vue";
import IconChevronRight from "@/components/icons/IconChevronRight.vue";
import IconBarsArrowUp from "@/components/icons/IconBarsArrowUp.vue";
import RoundCheckbox from "@/components/RoundCheckbox.vue";
import RetinaAnalysisCorrectModal from "@/components/RetinaAnalysisCorrectModal.vue";
import IconPencilSquare from '../components/icons/IconPencilSquare.vue';

const STEP_UPLOAD = 1; // Шаг загрузки изображения
const STEP_DETECTION = 2; // Шаг детекци изображения
const STEP_ANALYSIS = 3; // Шаг анализа изображения

const STATUS_READY = 1; // Статуст задачи - активна
const STATUS_PROGRESS = 2; // Статус задачи - в процессе
const STATUS_SUCCESS = 3; // Статус задачи - успешно выполнена
const STATUS_ERROR = 4; // Статус задачи - завершилась с ошибкой

// Вид отображения результата детекции - оригинальное изображение
const DETECTION_VIEW_MODE_ORIG = 0;
// Вид отображения результата детекции - разметка границ
const DETECTION_VIEW_MODE_BOXES = 1;

// Порядок сортировки по точности - возрастание
const SORT_STATE_SCORE_ASC = 0;
// Порядок сортировки по точности - убывание
const SORT_STATE_SCORE_DESC = 1;
// Порядок сортировки как в справочнике
const SORT_STATE_BOOK = 2;

export default {
  name: "DemoView",
  data() {
    return {
      /* Steps */
      STEP_UPLOAD: STEP_UPLOAD,
      STEP_DETECTION: STEP_DETECTION,
      STEP_ANALYSIS: STEP_ANALYSIS,

      /* Task statuses */
      STATUS_READY: STATUS_READY,
      STATUS_PROGRESS: STATUS_PROGRESS,
      STATUS_SUCCESS: STATUS_SUCCESS,
      STATUS_ERROR: STATUS_ERROR,

      /* Константы для отображения обложки распознавания границ детекции */
      DETECTION_VIEW_MODE_ORIG: DETECTION_VIEW_MODE_ORIG,
      DETECTION_VIEW_MODE_BOXES: DETECTION_VIEW_MODE_BOXES,

      /* Константы для сортировки групп с метками */
      SORT_STATE_SCORE_ASC: SORT_STATE_SCORE_ASC,
      SORT_STATE_SCORE_DESC: SORT_STATE_SCORE_DESC,
      SORT_STATE_BOOK: SORT_STATE_BOOK,

      /* Доступные примеры с ОКТ снимками в базе */
      examples: [],

      /**
       * Категории групп меток
       */
      labelGroups: [],

      /**
       * Признаки метки сетчатки
       */
      labelMarks: [],

      /**
       * Модальное окно с изображением
       */
      imageModalView: {
        isActive: false,
        src: "",
      },

      /**
       * Задача загрузки изображения
       */
      taskUpload: {
        image: {
          guid: "",
          imageURL: "",
          thumbnailURL: "",
        },
        status: STATUS_READY,
        statusText: "Изображение не выбрано",
      },

      /**
       * Задача распознавания сегментов на изображении
       */
      taskDetection: {
        id: {
          model: "",
          queue: "",
        },
        crops: [],
        meta: {
          cover: "",
        },
        isOBB: false,
        viewMode: DETECTION_VIEW_MODE_ORIG,
        status: STATUS_READY,
        statusText: "",
      },

      /**
       * Задача анализа наличия меток
       */
      taskAnalisis: {
        id: {
          model: "",
          queue: "",
        },
        /**
         * Сегменты анализа
         */
        crops: [],
        /**
         * Состояние выполнения анализа на сервере
         */
        progressState: [],
        /**
         * Массив с результатами
         */
        results: [],
        /**
         * Отформатированные данные для вывода
         */
        resultsFormat: [],
        /**
         * Результаты в каком виде желательно чтобы приходили
         */
        tmpResultsFormat: [
          {
            groupID: 0,
            name: "Первая группа",
            sortState: this.SORT_STATE_SCORE_ASC,
            isExpand: false,
            labels: [
              {
                id: 1,
                label: "koger_mak_retina_53",
                name: "Лабел 1",
                accuracy: 0.86,
                isSelect: true,
                sortIndex: 1,
                cropsVisible: true,
                crops: [
                  { id: 1, thumbnailURL: "", imageURL: "", accuracy: 0.76 },
                  { id: 2, thumbnailURL: "", imageURL: "", accuracy: 0.86 },
                ],
              },
              {
                id: 2,
                label: "koger_mak_retina_53",
                name: "Лабел 2",
                accuracy: 0.77,
                isSelect: true,
                sortIndex: 2,
                cropsVisible: true,
                crops: [
                  { id: 1, thumbnailURL: "", imageURL: "", accuracy: 0.77 },
                ],
              },
            ],
          },
          {
            groupID: 1,
            name: "Вторая группа",
            sortState: this.SORT_STATE_SCORE_ASC,
            isExpand: true,
            labels: [
              {
                id: 1,
                label: "koger_mak_retina_53",
                name: "Лабел 1",
                accuracy: 0.86,
                isSelect: true,
                sortIndex: 1,
                cropsVisible: true,
                crops: [
                  { id: 1, thumbnailURL: "", imageURL: "", accuracy: 0.76 },
                  { id: 2, thumbnailURL: "", imageURL: "", accuracy: 0.86 },
                ],
              },
              {
                id: 2,
                label: "koger_mak_retina_53",
                name: "Лабел 2",
                accuracy: 0.77,
                isSelect: true,
                sortIndex: 2,
                cropsVisible: true,
                crops: [
                  { cropID: 1, thumbnailURL: "", imageURL: "", accuracy: 0.77 },
                ],
              },
              {
                id: 3,
                label: "koger_mak_retina_53",
                name: "Лабел 3",
                accuracy: 0.86,
                isSelect: true,
                sortIndex: 3,
                cropsVisible: true,
                crops: [
                  { id: 1, thumbnailURL: "", imageURL: "", accuracy: 0.76 },
                  { id: 2, thumbnailURL: "", imageURL: "", accuracy: 0.86 },
                ],
              },
              {
                id: 4,
                label: "koger_mak_retina_53",
                name: "Лабел 4",
                accuracy: 0.77,
                isSelect: true,
                sortIndex: 4,
                cropsVisible: true,
                crops: [
                  { id: 1, thumbnailURL: "", imageURL: "", accuracy: 0.77 },
                ],
              },
            ],
          },
        ],
        /** Открыть модальное окно для коректирования результатов */
        isCorrected: false,
        /** Скорректированные результаты */
        correctedResults: {
          isCorrect: false,
          labels: [],
        },
        /** Статус */
        status: STATUS_READY,
        statusText: "",
      },
      /**
       * Задача скачивания отчета
       */
      taskReport: {
        reportText: "Дополнительная информация:\n",
        link: "",
        status: STATUS_READY,
        statusText: "",
      },
      /**
       * Фильтр порога точности
       */
      thresholdFilter: {
        value: 0.7,
        isExpand: false,
        tempValue: 70,
      },
    };
  },
  components: {
    CheckboxRadio,
    ImageModalWindow,
    IconImage,
    IconSquareStack,
    IconDocumentation,
    IconNumberedList,
    IconChevronRight,
    IconBarsArrowUp,
    RoundCheckbox,
    RetinaAnalysisCorrectModal,
    IconPencilSquare,
  },
  computed: {
    /**
     * URL к основному изображению
     */
    coverMainURL() {
      if (this.taskUpload.status == this.STATUS_SUCCESS) {
        if (this.taskDetection.viewMode == DETECTION_VIEW_MODE_BOXES) {
          return this.taskDetection.meta.cover;
        } else {
          return this.taskUpload.image.imageURL;
        }
      } else {
        return "";
      }
    },
    /**
     * Активный шаг выполнения
     */
    stepActive() {
      // Загрузка изображения
      if (this.taskUpload.status != STATUS_SUCCESS) {
        return STEP_UPLOAD;
      }
      // Распознавание сегментов
      if (
        this.taskUpload.status == this.STATUS_SUCCESS &&
        (this.taskDetection.status != this.STATUS_SUCCESS ||
          this.taskDetection.crops.length == 0)
      ) {
        return STEP_DETECTION;
      }
      // Анализ изображения
      if (
        this.taskDetection.status == this.STATUS_SUCCESS &&
        this.taskAnalisis != this.STATUS_SUCCESS &&
        this.taskDetection.crops.length > 0
      ) {
        return STEP_ANALYSIS;
      }
    },
    /**
     * Вывод текста в textarea
     */
    labelsResultText() {
      let text = "";
      let isLabelExists = false;
      let number = 1;
      for (let i = 0; i < this.taskAnalisis.resultsFormat.length; i++) {
        // идем по группам
        let groupResults = this.taskAnalisis.resultsFormat[i];
        let labelsSelected = groupResults.labels.filter(
          (label) => label.isSelect
        );
        if (labelsSelected.length > 0) {
          text += `${number++}. ${groupResults.name}: ${labelsSelected
            .map((label) => label.name)
            .join(", ")}.\r\n`;
          isLabelExists = true;
        }
      }
      text += `${isLabelExists ? "\r\n" : ""}Дополнительная информация:\r\n`;
      return text;
    },
    /**
     * Статус приложения
     */
    appStatus() {
      if (
        this.taskUpload.status == this.STATUS_PROGRESS ||
        this.taskDetection.status == this.STATUS_PROGRESS ||
        this.taskAnalisis.status == this.STATUS_PROGRESS
      ) {
        return this.STATUS_PROGRESS;
      } else {
        return this.STATUS_READY;
      }
    },
  },
  methods: {
    /**
     * Открыть модельное окно с изображением
     */
    openImageModal(imageURL) {
      this.imageModalView.isActive = true;
      this.imageModalView.src = imageURL;
    },
    /**
     * Закрыть модельное окно с изображением
     */
    closeImageModal() {
      this.imageModalView.isActive = false;
      this.imageModalView.src = "";
    },
    correctModalOpen() {
      if (this.taskAnalisis.correctedResults.isCorrect == false) {
        // Если результаты еще не были скорректирвоаны
        let currentAnalysisResult = {};
        for (let i = 0; i < this.taskAnalisis.crops.length; i++) {
          currentAnalysisResult[this.taskAnalisis.crops[i].id] = [];
        }
        for (let i = 0; i < this.taskAnalisis.resultsFormat.length; i++) {
          let resultGroup = this.taskAnalisis.resultsFormat[i];
          for (let j = 0; j < resultGroup.labels.length; j++) {
            let labelCurrent = resultGroup.labels[j];
            if (labelCurrent.isSelect == true) {
              for (let k = 0; k < labelCurrent.crops.length; k++) {
                let currentCrop = labelCurrent.crops[k];
                currentAnalysisResult[currentCrop.cropID].push(labelCurrent.id);
              }
            }
          }
        }
        this.$refs.correctModal.analysisResults = currentAnalysisResult;
        this.$refs.correctModal.initCropResults();
        this.taskAnalisis.isCorrected = true;
      } else {
        // Результаты уже скорректированы
        let currentAnalysisResult = {};
        for (let i = 0; i < this.taskAnalisis.crops.length; i++) {
          currentAnalysisResult[this.taskAnalisis.crops[i].id] = [];
        }
        // Значит есть массив с результатами
        for (let i = 0; i < this.taskAnalisis.correctedResults.labels.length; i++) {
          let labelResultIter = this.taskAnalisis.correctedResults.labels[i];
          currentAnalysisResult[labelResultIter.crop_id].push(labelResultIter.label_id);
        }
        this.$refs.correctModal.analysisResults = currentAnalysisResult;
        this.$refs.correctModal.initCropResults();
        this.taskAnalisis.isCorrected = true;
      }

    },
    correctModalClose() {
      this.taskAnalisis.isCorrected = false;
    },
    /**
     * Результаты были скорректирвоаны
     */
    correctUpdateResults() {
      this.taskAnalisis.isCorrected = false;
      this.taskAnalisis.correctedResults.isCorrect = this.$refs.correctModal.correctedResults.isCorrected;
      this.taskAnalisis.correctedResults.labels = this.$refs.correctModal.correctedResults.labels;
      this.$refs.correctModal.correctedResults.isCorrected = false;
      this.$refs.correctModal.correctedResults.labels = [];
      // Обновляем текст отчета смотря исправления
      let text = this.getCorrectedText();
      this.taskReport.reportText = text;
    },
    getCorrectedText() {
      let text = "";
      let isLabelExists = false;
      let number = 1;
      let labelResults = this.taskAnalisis.correctedResults.labels;
      for(let i=0; i<this.labelGroups.length;i++) {
        // Идем по группам и смотрим есть ли метки группы в исправленных результатах
        let labeGroup = this.labelGroups[i];
        let labelsSelected = labelResults.filter(l => l.label_group == labeGroup.id);
        if (labelsSelected.length > 0) {
          // Если есть метки группы в исправленных результатах
          isLabelExists = true;
          let labelSelectedNames = labelsSelected.map((l) => l.label_name);
          let labelSelectedNamesUniq = [];
          for(let k=0;k<labelSelectedNames.length;k++) {
            if(!labelSelectedNamesUniq.includes(labelSelectedNames[k])) {
              labelSelectedNamesUniq.push(labelSelectedNames[k]);                 
            }
          }
          text += `${number++}. ${labeGroup.name}: ${
            labelSelectedNamesUniq.join(", ")}.\r\n`;
        }
      }
      text += `${isLabelExists ? "\r\n" : ""}Дополнительная информация:\r\n`;
      return text;
    },
    plural(number, single, double, plural) {
      number = parseInt(number);
      var cases = [2, 0, 1, 1, 1, 2];
      var texts = [single, double, plural];
      return texts[
        number % 100 >= 5 && number % 100 < 20
          ? 2
          : cases[Math.min(number % 10, 5)]
      ];
    },
    /**
     * Получение примером ОКТ снимков из БД
     */
    getExamples() {
      axios
        .get("/api/v1/retinadeepai/constants/examples/")
        .then((response) => {
          this.examples = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    /**
     * Получение групп ОКТ маркеров
     */
    getLabelTypes() {
      axios
        .get("/api/v1/retinadeepai/constants/label-groups/")
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
      axios
        .get("/api/v1/retinadeepai/constants/label-marks/")
        .then((response) => {
          this.labelMarks = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    /**
     * Инициализация задачи загрузки файла
     */
    initTaskUpload() {
      this.taskUpload.status = STATUS_READY;
      this.taskUpload.statusText = "";
      this.taskUpload.image.guid = "";
      this.taskUpload.image.imageURL = "";
      this.taskUpload.image.thumbnailURL = "";
    },
    /**
     * Инициализация задачи детекции
     */
    initTaskDetection() {
      this.taskDetection.status = STATUS_READY;
      this.taskDetection.id.model = "";
      this.taskDetection.id.queue = "";
      this.taskDetection.statusText = "";
      this.taskDetection.viewMode = "orig";
      this.taskDetection.crops = [];
    },
    /**
     * Инициализация задачи анализа результатов
     */
    initTaskAnalisis() {
      this.taskAnalisis.status = STATUS_READY;
      this.taskAnalisis.statusText = "";
      this.taskAnalisis.crops = [];
      this.taskAnalisis.correctedResults.isCorrect = false;
      this.taskAnalisis.correctedResults.labels = [];
    },
    /**
     * Инициализация приложения
     */
    initDemoApp() {
      this.initTaskAnalisis(); // чистим задачу анализа картинки
      this.initTaskDetection(); // чистим задачу детекции
      this.initTaskUpload(); // чистим загрузку файла
    },
    /**
     * Кнопка загрузить файл
     */
    chooseFile() {
      document.getElementById("fileUpload").click();
    },
    /**
     * Открыть примеры
     */
    viewExamples() {
      this.initDemoApp();
      this.isSelectExample = true;
    },
    /**
     * Выбор примера
     */
    selectExample(example) {
      this.isSelectExample = false;
      this.taskUpload.status = STATUS_SUCCESS;
      this.taskUpload.statusText = "Изображение загружено";
      this.taskUpload.image.guid = example.guid;
      this.taskUpload.image.imageURL = example.get_image;
      this.taskUpload.image.thumbnailURL = example.get_thumbnail;
    },
    /**
     * Загрузка изображения
     */
    uploadImage(inputFileID) {
      var fileUploader = document.getElementById(inputFileID);

      if (fileUploader.files == null || fileUploader.files.length == 0) {
        return;
      }

      var formData = new FormData();
      formData.append("file", fileUploader.files[0]);

      this.initDemoApp();
      this.isSelectExample = false;

      if (fileUploader.files[0].size / 1024 / 1024 > 3) {
        this.taskUpload.status = STATUS_ERROR;
        this.taskUpload.statusText =
          "Размер изображения не должен превышать 3МБ";
        return;
      }

      this.taskUpload.status = STATUS_PROGRESS;
      this.taskUpload.statusText = "Идет загрузка изображения";

      axios({
        method: "post",
        url: "/api/v1/retinadeepai/upload/",
        data: formData,
        headers: { "Content-Type": "multipart/form-data" },
      })
        .then((response) => {
          this.taskUpload.status = STATUS_SUCCESS;
          this.taskUpload.statusText = "Изображение загружено";
          this.taskUpload.image.guid = response.data.guid;
          this.taskUpload.image.imageURL = response.data.get_image;
          this.taskUpload.image.thumbnailURL = response.data.get_thumbnail;
        })
        .catch((error) => {
          this.taskUpload.status = this.STATUS_ERROR;
          if (error.response) {
            this.taskUpload.statusText = error.response.data.message;
          } else if (error.request) {
            this.taskUpload.statusText = error.message;
          } else {
            this.taskUpload.statusText = error.message;
          }
        });
    },
    /**
     * Отправить запрос на сервер для распознавания сегментов
     */
    detectionFile() {
      this.initTaskAnalisis();
      this.initTaskDetection();
      this.taskDetection.status = this.STATUS_PROGRESS;

      const form = new FormData();
      form.append("image_guid", this.taskUpload.image.guid);
      form.append("is_obb", this.taskDetection.isOBB ? 1 : 0);
      axios({
        method: "post",
        url: "/api/v1/retinadeepai/detection/",
        data: form,
      })
        .then((response) => {
          this.taskDetection.id.model = response.data.data.task_model_id;
          this.taskDetection.id.queue = response.data.data.task_queue_id;
          this.taskDetection.statusText = response.data.message;

          this.getStatusDetectionTask(this.taskDetection.id.queue);
        })
        .catch((error) => {
          this.taskDetection.status = this.STATUS_ERROR;
          if (error.response) {
            this.taskDetection.statusText = error.response.data.message;
          } else if (error.request) {
            this.taskDetection.statusText = error.message;
          } else {
            this.taskDetection.statusText = error.message;
          }
        });
    },
    /**
     * Получения статуста задачи детекции
     */
    getStatusDetectionTask(task_id) {
      let app = this;
      axios({
        method: "get",
        url: `/api/v1/retinadeepai/detection/tasks/${task_id}/`,
      })
        .then((response) => {
          if (response.data.task_status == "SUCCESS") {
            // ставим все как выбранные фрагменты
            let crops = response.data.results.crops;
            for (let i = 0; i < crops.length; i++) {
              crops[i].select = true;
            }
            app.taskDetection.crops = response.data.results.crops;
            if (response.data.results.crops.length > 0) {
              app.taskDetection.viewMode = DETECTION_VIEW_MODE_BOXES;
              app.taskDetection.meta.cover =
                response.data.results.task.get_detection_cover;
            }
            app.taskDetection.status = app.STATUS_SUCCESS;
            app.taskDetection.statusText = response.data.message;
            return true;
          } else if (response.data.task_status == "FAILURE") {
            app.taskDetection.status = app.STATUS_ERROR;
            app.taskDetection.statusText = response.data.message;
            return false;
          }
          app.taskDetection.statusText = response.data.message;
          // rerun every 2 seconds
          setTimeout(function () {
            app.getStatusDetectionTask(task_id);
          }, 1500);
        })
        .catch((error) => {
          this.taskDetection.status = this.STATUS_ERROR;
          if (error.response) {
            this.taskDetection.statusText = error.response.data.message;
          } else if (error.request) {
            this.taskDetection.statusText = error.message;
          } else {
            this.taskDetection.statusText = error.message;
          }
        });
    },
    /**
     * Отправить запрос на сервер для анализа
     */
    analysisFile() {
      this.initTaskAnalisis();
      this.taskAnalisis.status = this.STATUS_PROGRESS;
      this.taskAnalisis.statusText = "Начинаем анализ изображения";

      let json_data = {
        task_detection: this.taskDetection.id.model,
        crops: this.taskDetection.crops
          .filter((item) => item.select)
          .map((item) => item.id),
      };

      axios({
        method: "post",
        url: "/api/v1/retinadeepai/analysis/",
        data: JSON.stringify(json_data),
      })
        .then((response) => {
          this.taskAnalisis.id.model = response.data.data.task_model_id;
          this.taskAnalisis.id.queue = response.data.data.task_queue_id;
          this.taskAnalisis.statusText = response.data.message;

          this.getStatusAnalysisTask(this.taskAnalisis.id.queue);
        })
        .catch((error) => {
          this.taskAnalisis.status = this.STATUS_ERROR;
          console.log(error);
          if (error.response) {
            this.taskAnalisis.statusText = this.STATUS_ERROR;
            this.taskAnalisis.statusText = error.response.data.message;
          } else if (error.request) {
            this.taskAnalisis.statusText = this.STATUS_ERROR;
            this.taskAnalisis.statusText = error.message;
          } else {
            this.taskAnalisis.statusText = this.STATUS_ERROR;
            this.taskAnalisis.statusText = error.message;
          }
        });
    },
    /**
     * Получения статуста задачи детекции
     */
    getStatusAnalysisTask(task_id) {
      let app = this;
      axios({
        method: "get",
        url: `/api/v1/retinadeepai/analysis/tasks/${task_id}/`,
      })
        .then((response) => {
          console.log(response);
          if (response.data.task_status == "SUCCESS") {
            // результаты есть
            // получаем результат
            app.taskAnalisis.results = response.data.results;
            app.taskAnalisis.resultsFormat = this.preparePrettyAnalysisResult(
              response.data.results
            );
            app.taskAnalisis.progressState = response.data.progressState;
            app.taskAnalisis.statusText = response.data.message;
            app.taskAnalisis.status = this.STATUS_SUCCESS;
            app.taskAnalisis.crops = app.taskDetection.crops.filter(crop => crop.select);
            app.updateReportTextByMark();
            return true;
          } else if (response.data.task_status == "FAILURE") {
            app.taskAnalisis.status = app.STATUS_ERROR;
            app.taskAnalisis.statusText = response.data.message;
            return false;
          } else if (response.data.task_status == "PROGRESS") {
            app.taskAnalisis.statusText = response.data.message;
          }
          console.log(response);
          // rerun every 2.5 seconds
          setTimeout(function () {
            app.getStatusAnalysisTask(task_id);
          }, 2500);
        })
        .catch((error) => {
          this.taskAnalisis.status = this.STATUS_ERROR;
          if (error.response) {
            this.taskAnalisis.statusText = error.response.data.message;
          } else if (error.request) {
            this.taskAnalisis.statusText = error.message;
          } else {
            this.taskAnalisis.statusText = error.message;
          }
        });
    },
    /**
     * Преобразование результатов в виде массива в удобный формат для вывода и выбора меток
     */
    preparePrettyAnalysisResult(resultsList) {
      // собираем метки
      let labelResultsDict = {};
      resultsList = resultsList.filter(
        (item) => item.score >= this.thresholdFilter.value
      );
      for (let i = 0; i < resultsList.length; i++) {
        if (labelResultsDict[resultsList[i]["label_mark"]] !== undefined) {
          labelResultsDict[resultsList[i]["label_mark"]].push(resultsList[i]);
        } else {
          labelResultsDict[resultsList[i]["label_mark"]] = [resultsList[i]];
        }
      }

      let resultsLabelMarkExists = [];
      for (let i = 0; i < this.labelMarks.length; i++) {
        if (labelResultsDict[this.labelMarks[i].label] !== undefined) {
          let resultsExists = labelResultsDict[this.labelMarks[i].label];
          // есть результаты по данной метке
          let labelCurrent = {
            id: this.labelMarks[i].id,
            label: this.labelMarks[i].label,
            groupID: this.labelMarks[i].group_id,
            name: this.labelMarks[i].name,
            accuracy: 0.0,
            isSelect: true,
            sortIndex: this.labelMarks[i].sort_index,
            cropsVisible: false,
            crops: [],
          };

          let labelAccuracy = 0.0;
          for (let j = 0; j < resultsExists.length; j++) {
            if (labelAccuracy < resultsExists[j].score) {
              labelAccuracy = resultsExists[j].score;
            }
            labelCurrent.crops.push({
              id: resultsExists[j].crop_analysis,
              thumbnailURL: resultsExists[j].get_thumbnail,
              imageURL: resultsExists[j].get_image,
              accuracy: resultsExists[j].score,
              cropID: resultsExists[j].crop_id,
            });
          }
          labelCurrent.accuracy = labelAccuracy;
          resultsLabelMarkExists.push(labelCurrent);
        }
      }

      // собираем в группы
      let groupResultsFormat = [];
      for (let i = 0; i < this.labelGroups.length; i++) {
        let groupID = this.labelGroups[i].id;
        let labelGroups = resultsLabelMarkExists.filter(
          (label) => label.groupID == groupID
        );
        if (labelGroups.length > 0) {
          // есть метки группы
          let groupResult = {
            id: groupID,
            name: this.labelGroups[i].name,
            sortState: "guide",
            isExpand: false,
            sortIndex: this.labelGroups[i].sort_index,
            labels: labelGroups,
          };
          groupResultsFormat.push(groupResult);
        }
      }

      return groupResultsFormat;
    },
    updateThreasholdValue() {
      let tempResults = this.preparePrettyAnalysisResult(this.taskAnalisis.results);
      this.taskAnalisis.resultsFormat = tempResults;
      this.updateReportTextByMark();
    },
    /**For animations */
    enter(element) {
      const width = getComputedStyle(element).width;

      element.style.width = width;
      element.style.position = "absolute";
      element.style.visibility = "hidden";
      element.style.height = "auto";

      const height = getComputedStyle(element).height;

      element.style.width = null;
      element.style.position = null;
      element.style.visibility = null;
      element.style.height = 0;

      // Force repaint to make sure the
      // animation is triggered correctly.
      getComputedStyle(element).height;

      // Trigger the animation.
      // We use `requestAnimationFrame` because we need
      // to make sure the browser has finished
      // painting after setting the `height`
      // to `0` in the line above.
      requestAnimationFrame(() => {
        element.style.height = height;
      });
    },
    afterEnter(element) {
      element.style.height = "auto";
    },
    leave(element) {
      const height = getComputedStyle(element).height;

      element.style.height = height;

      // Force repaint to make sure the
      // animation is triggered correctly.
      getComputedStyle(element).height;

      requestAnimationFrame(() => {
        element.style.height = 0;
      });
    },

    /**For ContentExpander */
    sortLabelMarks(labelGroups, sortState) {
      if (sortState == this.SORT_STATE_BOOK)
        return labelGroups.sort(function (a, b) {
          return a.sortIndex - b.sortIndex;
        });
      else if (sortState == this.SORT_STATE_SCORE_ASC)
        return labelGroups.sort(function (a, b) {
          return a.accuracy - b.accuracy;
        });
      else
        return labelGroups.sort(function (a, b) {
          return b.accuracy - a.accuracy;
        });
    },
    /**
     * Обновление текста в тексте отчета при изменении метки
     */
    updateReportTextByMark() {
      let reportTextNew = "";
      let searchDelimetr = "Дополнительная информация:";
      let indexDopInfo = this.taskReport.reportText
        .toLocaleLowerCase()
        .indexOf(searchDelimetr.toLocaleLowerCase());
      if (indexDopInfo == -1) {
        reportTextNew = this.labelsResultText;
      } else {
        reportTextNew =
          this.labelsResultText +
          this.taskReport.reportText
            .slice(indexDopInfo + searchDelimetr.length)
            .trim();
      }
      this.taskReport.reportText = reportTextNew;
    },
    /**
     * Генерация отчета
     */
    generateReport() {
      this.taskReport.status = this.STATUS_PROGRESS;
      const form = new FormData();
      let decription = this.taskReport.reportText
      form.append('description', decription);
      axios({
        method: 'post',
        url: `/api/v1/retinadeepai/generate-report/${this.taskAnalisis.id.model}/`,
        data: form,
        responseType: 'blob'
      })
        .then(response => {
          this.taskReport.status = STATUS_SUCCESS;
          const url = window.URL.createObjectURL(response.data);
          const link = document.createElement('a');
          link.href = url;
          link.setAttribute('download', 'report.docx');
          document.body.appendChild(link);
          link.click();
        })
        .catch(error => {
          this.taskReport.status = this.STATUS_ERROR;
          if (error.response) {
            this.taskReport.statusText = error.response.data.message;
          } else if (error.request) {
            this.taskReport.statusText = error.message;
          } else {
            this.taskReport.statusText = error.message;
          }
        });
    },
  },
  mounted() {
    this.getExamples();
    this.getLabelTypes();
    this.getAvailableLabels();
  },
};
</script>

<style scoped>
.retina-app {
  display: flex;
  flex-flow: row nowrap;
  color: #494949;
}

.retina-app__sidebar {
  max-width: 510px;
  min-width: 310px;
  flex: 1 1 510px;
}

.retina-app__body {
  flex: 1 1 auto;
  display: flex;
  flex-flow: column nowrap;
  padding: 0 2rem;
}

.retina-menu {
  border-radius: 5px;
  box-shadow: 0px 0rem 12px 0rem rgba(10, 10, 10, 0.1),
    0 0px 0 1px rgba(10, 10, 10, 0.02);
}

.retina-menu__item {}

.retina-image-container {
  display: flex;
  margin-bottom: 1.5rem;
  justify-content: center;
  align-items: center;
}

.retina-crop {}

.retina-crop__cover {
  width: 54px;
  min-width: 54px;
  height: 32px;
  min-height: 32px;
  object-fit: cover;
}

.retina-crop__status {
  margin-top: 0.25rem;
  text-align: right;
  font-size: 0.8rem;
}

/*#region ContentExpander */

.content-expander {
  display: flex;
  flex-flow: column nowrap;
  border: 1px solid #e4edfd;
  border-radius: 5px;
  overflow: hidden;
}

.content-expander_expand .content-expander__header {
  background-color: #c3d6f9;
}

.content-expander__header {
  display: flex;
  flex-flow: row nowrap;
  justify-content: space-between;
  color: #2d2f32;
  padding-bottom: 1px;
  transition: all ease-in-out 0.15s;
  padding: 0.5rem;
  background-color: #e4ebf7;
  cursor: pointer;
}

.content-expander__title {
  display: flex;
  flex-flow: row nowrap;
  align-items: center;
  color: #294b8b;
  font-size: 15px;
}

.content-expander__icon {
  text-align: center;
  margin-right: 10px;
  font-weight: 900;
  vertical-align: baseline;
}

.content-expander__actions {
  display: flex;
  flex-flow: row-reverse wrap;
  padding: 0.5rem 0.5rem 0 0.5rem;
  align-items: center;
}

.content-expander__body {}

.expander-action {
  display: inline-flex;
  flex-flow: row nowrap;
  padding: 0.35rem 0.75rem;
  background-color: #fbfdff;
  border: 1px solid #f2f3f9;
  border-radius: 3px;
}

.expander-action__icon {
  padding: 2px;
  width: 22px;
  height: 22px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.expander-action__icon:hover {
  color: #3170d1;
  background-color: #fff;
}

.expander-action__icon_selected {
  color: #1d62c9;
}

.expander-action__icon_selected:hover {
  color: #1d62c9;
  background: initial;
}

.expander-action__title {}

.expand-enter-active,
.expand-leave-active {
  transition: height 0.4s ease-in-out;
  overflow: hidden;
}

.expand-enter,
.expand-leave-to {
  height: 0;
}

.content-expander__table {
  padding: 0.5rem;
}

.content-expander__table {
  display: flex;
  flex-flow: column nowrap;
  width: 100%;
}

.expander-table-row {
  display: flex;
  flex-flow: column nowrap;
}

.expander-table-row__header {
  display: flex;
  flex-flow: nowrap;
  align-items: center;
}

.expander-table-row__title {
  border-bottom: 1px dashed;
}

.expander-table-row__expand {
  border: none;
}

.expander-table-row__title:hover {
  color: #0d64d3;
  cursor: pointer;
}

.expander-table-row__body {
  display: flex;
}

/*#enregion ContentExpander */

@media (max-width: 900px) {
  .retina-app {
    flex-flow: column nowrap;
  }

  .retina-app__sidebar {
    max-width: none;
    flex: 1 1 auto;
    margin-bottom: 2rem;
  }

  .retina-app__body {
    padding: 0;
  }
}
</style>