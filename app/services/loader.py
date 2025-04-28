from app.extensions import db
from app.models import Finance
from app.extensions.logger import logger


def deleted_finance_data_db():
    """
    Полное удаление старых финансовых данных из базы данных.
    """
    try:
        logger.info("Начало удаления старых финансовых данных.")
        info_delete = Finance.query.all()
        for item in info_delete:
            db.session.delete(item)
            logger.debug(f"Удалён объект данных: {item}")

        db.session.commit()
        logger.info("Старые финансовые данные успешно удалены из базы данных.")
    except Exception as e:
        logger.error(f"Ошибка при удалении старых финансовых данных из базы данных: {e}")
        db.session.rollback()  # Откат изменений в случае ошибки


def insert_finance_data_db(res_dict):
    """
    Вставка финансовых данных в базу данных.
    При вставке происходит полное удаление старых записей и добавление новых.
    """
    try:
        logger.info("Начало обработки вставки финансовых данных в базу данных.")
        # Удаление существующих данных
        deleted_finance_data_db()
        logger.info("Старые данные успешно удалены.")

        # Добавление новых данных
        for item in res_dict.values():
            try:
                financial_data = Finance(
                    id=item['area_number'],
                    area_number=item['area_number'],
                    member_fee=item.get('member_fee', 0.0),  # Значение по умолчанию - 0.0
                    targeted_fee=item.get('targeted_fee', 0.0),  # Значение по умолчанию - 0.0
                    electricity_payments=item.get('electricity_payments', 0.0),  # Значение по умолчанию - 0.0
                    published=item['date']
                )
                db.session.add(financial_data)
                logger.debug(f"Добавлены финансовые данные для участка {item['area_number']}.")
            except KeyError as e:
                logger.error(f"Отсутствует обязательное поле в данных для участка: {e}")
                continue  # Пропустить текущую итерацию, чтобы не прерывать обработку всей структуры res_dict

        # Коммит изменений в базу данных
        db.session.commit()
        for k, v in res_dict.items():
            logger.debug(f"Участок - {k}: {v}")
        logger.info("Все новые финансовые данные успешно добавлены в базу данных.")
    except Exception as e:
        logger.error(f"Ошибка при вставке финансовых данных в базу данных: {e}")
        db.session.rollback()  # Откат изменений в случае ошибки
