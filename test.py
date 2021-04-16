import logging

logging.basicConfig(
     format='%(asctime)s [%(levelname)s] %(message)s - %(filename)s:%(lineno)d',
    level=logging.DEBUG)

from koapy import KiwoomOpenApiPlusEntrypoint


with KiwoomOpenApiPlusEntrypoint() as context:
    # 로그인 처리
    context.EnsureConnected()

    # 이벤트를 알아서 처리하고 결과물만 제공하는 상위 함수 사용 예시
    # code = '005930'
    # info = context.GetStockBasicInfoAsDict(code)
    # print(info)
    # price = info['현재가']
    # print(price)

    # info = context.GetDailyStockDataAsDataFrame('005930')
    # print('일봉:')
    # print(info)

    # 이벤트를 스트림으로 반환하는 하위 함수 직접 사용 예시 (위의 상위 함수 내부에서 실제로 처리되는 내용에 해당)
    rqname = '업종별주가요청'
    # trcode = 'OPT10001'
    trcode = 'OPT20002'
    screenno = '0073'
    inputs = {'시장구분': '0', '업종코드': '013'}
    single = {}
    multi = []
    # 아래의 함수는 gRPC 서비스의 rpc 함수를 직접 호출함
    # 따라서 event 메시지의 구조는 koapy/backend/kiwoom_open_api_plus/grpc/KiwoomOpenApiPlusService.proto 파일 참조
    for event in context.TransactionCall(rqname, trcode, screenno, inputs):
        names = event.single_data.names
        values = event.single_data.values
        multi_names = event.multi_data.names
        multi_values = event.multi_data.values
        for name, value in zip(names, values):
            single[name] = value

        for name, value in zip(multi_names, multi_values):
            temp_dict = {}
            for n, v in zip(names, value.values):
                temp_dict[n] = v
            multi.append(temp_dict)
    # 전체 결과 출력 (싱글데이터)
    print('Got OPT2002 Tr Data (using TransactionCall):')
    print(single)
    print(multi)
    # 현재가 값만 출력
    # price = output['현재가']
    # print(price)
