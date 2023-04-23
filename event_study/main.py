# from event_study import download,mk_event, mk_ret, mk_cars, test_hypo
#
# def main(tic, update_csv=True):
#
#     if update_csv is True:
#         download.get_date(tic)
#     else:
#         print("skip download....")
#
#     ret_df = mk_ret.mk_ret_df(tic)
#
#     event_df = mk_event.mk_event_df(tic)
#
#     cars_df = mk_cars.mk_car_df(tic)
#
#     res = test_hypo.cal_hypo(cars_df)
#
#     print(res)
#
# if __name__ == "__main__":
#     tic = 'TSLA'
#     update_csv = True
#     main(tic=tic, update_csv=update_csv)