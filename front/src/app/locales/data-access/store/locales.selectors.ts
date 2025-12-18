import { localesFeature } from './locales.reducer';

export const {
  selectItems: selectLocalesItems,
  selectStatus: selectLocalesStatus,
  selectError: selectLocalesError,
  selectPage: selectLocalesPage,
  selectPageSize: selectLocalesPageSize,
  selectTotal: selectLocalesTotal,
  selectTotalPages: selectLocalesTotalPages,
  selectFilters: selectLocalesFilters,
} = localesFeature;
