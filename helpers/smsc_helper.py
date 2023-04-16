import smpplib.gsm
import smpplib.client
import smpplib.consts
import logging


class SMSCHelper:
    def __init__(self, host: str, port: int, system_id: str, password: str, source_number: str):
        self.client = smpplib.client.Client(host, port)
        self.client.connect()
        self.client.bind_transceiver(system_id=system_id, password=password)
        self.source_number = source_number

    def send_short_message(self, message: str, destination_number: str) -> bool:
        logger = logging.getLogger('smsc')
        try:
            logger.info("Enviando {0} a {1}".format(message, destination_number))
            self.client.send_message(sync_mode="async", addr_ton=smpplib.consts.SMPP_TON_ALNUM,
                                     addr_npi=smpplib.consts.SMPP_NPI_ISDN,
                                     source_addr_ton=smpplib.consts.SMPP_TON_ALNUM,
                                     source_addr_npi=smpplib.consts.SMPP_NPI_ISDN, source_addr=self.source_number,
                                     dest_addr_ton=smpplib.consts.SMPP_TON_UNK,
                                     dest_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
                                     destination_addr=destination_number,
                                     short_message=str.encode(message, 'utf8'))

            logger.info("Enviado {0} a {1}".format(message, destination_number))
            return True
        except Exception as error:
            logger.info("Error enviando {0} a {1}, error: {2}".format(message, destination_number, str(error)))
            return False
