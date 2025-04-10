import inspect
import json
import logging
import os
import sys

from app.config import LOG_FORMAT
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler

load_dotenv()

# Получаем текущее окружение
env = os.getenv("FLASK_ENV", "dev")

# # Подгрузка конфигурации и установка уровня логов
# try:
#     if env == "prod":
#         app.config.from_object('app.config.prod')
#         logger.info("Загружена конфигурация: Production")
#     elif env == "test":
#         app.config.from_object('app.config.test')
#         logger.info("Загружена конфигурация: Testing")
#     else:
#         app.config.from_object('app.config.dev')
#         logger.info("Загружена конфигурация: Development")
# except Exception as e:
#     logger.error(f"Ошибка загрузки конфигурации: {str(e)}")

# Устанавливаем уровень логов
if env == "prod":
    LOG_LEVEL = 'ERROR'
elif env == "test":
    LOG_LEVEL = 'INFO'
else:  # dev
    LOG_LEVEL = 'DEBUG'

CUSTOM_LOG_LEVELS = {
    logging.DEBUG: 100,
    logging.INFO: 200,
    logging.WARNING: 300,
    logging.ERROR: 400,
    logging.CRITICAL: 500,
}

NOTICE_LEVEL = 250


def initialize_notice_level():
    """
    Инициализирует уровень логирования NOTICE и добавляет пользовательский метод логирования для работы с этим уровнем.

    Определяет новый пользовательский уровень логирования и добавляет его в модуль logging.
    Добавляет метод `notice` в класс Logger, чтобы можно было логировать сообщения с
    использованием пользовательского уровня NOTICE.

    Устанавливает имя модуля, в котором сформировано лог-сообщение уровня NOTICE. Добавляет его в словарь extra,
    используемый в стандартном логгере Python.

    :return: None
    """
    logging.NOTICE = NOTICE_LEVEL
    logging.addLevelName(NOTICE_LEVEL, "NOTICE")

    def notice(self, message, *args, **kwargs):
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        module_name = module.__name__ if module else "unknown_module"
        if 'extra' not in kwargs:
            kwargs['extra'] = {}
        kwargs['extra']['custom_module'] = module_name
        if self.isEnabledFor(NOTICE_LEVEL):
            self._log(NOTICE_LEVEL, message, args, **kwargs)

    logging.Logger.notice = notice


initialize_notice_level()


class CustomFormatter(logging.Formatter):
    """
    Этот класс форматировщик лог-сообщений, наследующийся от logging.Formatter. Предназначенный для
    улучшения сообщений логирования за счёт добавления дополнительных полей, таких как уникальные
    идентификаторы логов, пользовательские уровни логов и гибкого форматирования вывода. Класс
    предоставляет возможности для JSON-форматирования с учетом кириллических символов и генерации
    последовательных идентификаторов логов для всех записей.

    :ivar log_counter: Отслеживает глобальный уникальный идентификатор логов для каждой записи лога.
    :type log_counter: int

    """
    log_counter = 99_999

    @classmethod
    def get_next_log_id(cls):
        """
        Эта функция создает сквозной счетчик для всех лог-сообщений. Предназначена для обеспечения
        уникальности каждого идентификатора лога при каждом вызове.

        Метод обновляет значение счётчика, хранящегося на уровне класса, и возвращает его.

        :return: Следующий уникальный log_id.
        :rtype: int
        """

        cls.log_counter += 1
        return cls.log_counter

    def __init__(self, fmt=None, datefmt=None, style='%', output_format='text'):
        super().__init__(fmt, datefmt, style)
        self.log_counter = self.get_next_log_id()
        self.output_format = output_format

    def format(self, record: logging.LogRecord) -> str:
        """
        Форматирует запись лог-сообщения в заданный текстовый или JSON-формат в зависимости
        от указанного формата вывода. Этот метод расширяет стандартную запись лога, добавляя
        уникальный идентификатор лога, пользовательский уровень логирования и дополнительные
        метаданные. Конечный результат либо соответствует формату JSON, либо форматированной
        строке, в зависимости от конфигурации объекта.

        :param record: Объект logging.LogRecord, содержащий всю информацию, относящуюся к событию,
                       которое логируется. Это включает сообщение, уровень логирования, имя модуля
                       и любые другие метаданные. Метод изменяет запись, добавляя уникальный
                       идентификатор лога и модифицированный уровень логирования.
        :type record: logging.LogRecord
        :return: Строковое представление форматированной записи лога. Если атрибут output_format
                 установлен как 'json', то возвращается строка в формате JSON. В противном случае
                 возвращается человекочитаемая форматированная строка.
        :rtype: str
        """

        record.log_id = self.get_next_log_id()
        record.custom_level_no = CUSTOM_LOG_LEVELS.get(record.levelno, record.levelno)

        if record.levelname == "WARNING":
            record.levelname = "WARN"
        elif record.levelname == "INFO":
            record.levelname = "INFO"

        # Получение имени модуля для уровня логов NOTICE и остальных
        module_name = getattr(record, 'custom_module').split('.')[-1] if hasattr(record, 'custom_module') else None
        if not module_name:
            module_name = record.module if hasattr(record, 'module') else 'unknown'

        log_record = {
            "datetime": f"[{self.formatTime(record)}]",
            "log_id": f"[log_id - {record.log_id}]",
            "level_num": record.custom_level_no,
            "level_name": record.levelname,
            "module": f"[module - {module_name}]",
            "message": record.getMessage(),
        }

        if self.output_format == 'json':
            return json.dumps(log_record, ensure_ascii=False)
        else:
            return (
                f"{log_record['datetime']} {log_record['level_num']} {log_record['level_name']} "
                f"{log_record['log_id']} {log_record['module']} {log_record['message']}"
            )


def get_handler(log_format: str) -> logging.Handler:
    """
    Возвращает обработчик логирования, настроенный на основе указанного формата логов
    (log_format). Функция настраивает и возвращает обработчик, подходящий для записи
    логов в файл или вывода в стандартный поток.

    :param log_format: Указывает формат логов. Если задано json, логи будут записываться
                       в файл в формате JSON. Если задано text, логи будут записываться
                       в файл в текстовом формате. Любое другое значение приведет к выведению
                       логов в стандартный поток в текстовом формате.

    :type log_format: str
    :return: Экземпляр обработчика логирования, настроенного на выполнение логирования с
             соответствующим форматом в зависимости от значения log_format.
    :rtype: logging.Handler
    """

    # абсолютные пути к директории приложения
    base_dir = os.path.dirname(os.path.abspath(__file__))  # app/extensions

    # Путь к лог-файлам
    logs_path_json = os.path.join(base_dir, '../logs/logfile_json.log')
    logs_path_text = os.path.join(base_dir, '../logs/logfile_text.log')
    log_path_rotation = os.path.join(base_dir, '../logs/application.log')

    # Создаем директорию, если её нет
    os.makedirs(os.path.dirname(log_path_rotation), exist_ok=True)

    # Настройка handler в зависимости от log_format
    if log_format == 'rotation':
        handler = RotatingFileHandler(log_path_rotation, maxBytes=1024 * 1024 * 10, backupCount=5)
        formatter = CustomFormatter(output_format=log_format)

    elif log_format == 'json':
        handler = logging.FileHandler(logs_path_json, mode='w', encoding='utf-8')
        formatter = CustomFormatter(
            output_format=log_format)  # Параметры не передаем, так как они определены в кастомном классе
    elif log_format == 'text':
        handler = logging.FileHandler(logs_path_text, mode='w', encoding='utf-8')
        formatter = CustomFormatter(output_format=log_format)
    else:
        handler = logging.StreamHandler(sys.stdout)
        formatter = CustomFormatter()

    handler.setFormatter(formatter)
    return handler


def create_logger(log_level: str, log_format: str = None) -> logging.Logger:
    """
    Создает и настраивает логгер с указанным уровнем логирования и форматом вывода.
    Настройки логгера включают проверку корректности уровня логирования, установку
    уровня по умолчанию в случае некорректного значения и выбор заданного формата
    вывода логов либо стандартного вывода по умолчанию.


    :param log_level: Уровень логирования в виде строки, представляющей один из
                      уровней модуля logging (DEBUG, INFO, WARNING и т.д.).
    :type log_level: str
    :param log_format: Формат вывода логов, может принимать значения json, text или stdout.
    :type log_format: str
    :return: Настроенный экземпляр логгера.
    :rtype: logging.Logger
    """

    # Создание временного логгера
    custom_logger = logging.getLogger('multi_format_logger')
    temp_handler = logging.StreamHandler(sys.stdout)
    formatter = CustomFormatter()
    temp_handler.setFormatter(formatter)
    custom_logger.addHandler(temp_handler)

    # Проверка наличия корректной переменной с уровнем логирования
    try:
        level_num = getattr(logging, log_level.upper())
        custom_logger.setLevel(level_num)
        # Уменьшение значения log_counter на 1 если все удачно
        CustomFormatter.log_counter -= 1
    except AttributeError:
        custom_logger.setLevel(logging.INFO)
        custom_logger.warning(f'Уровень логирования {log_level} некорректен. Установлен уровень по-умолчанию: INFO')

    # Проверка наличия корректной переменной с форматом логирования
    if not log_format or log_format.lower() not in ['json', 'text', 'rotation', 'stdout']:
        custom_logger.warning(f'Формат логирования не задан/задан некорректно. Установлен формат по-умолчанию: stdout')
    else:
        # Уменьшение значения log_counter на 1 если все удачно
        CustomFormatter.log_counter -= 1

    # Удаление временного логгера
    custom_logger.removeHandler(temp_handler)

    # Установка формата логирования
    handler = get_handler(log_format)
    custom_logger.addHandler(handler)

    return custom_logger


logger = create_logger(
    log_level=LOG_LEVEL,
    log_format=LOG_FORMAT
)
