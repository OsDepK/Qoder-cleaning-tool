#!/usr/bin/env python3
"""
Clean-Qoder - 专业清理工具
版本: 1.0
重置 Qoder 应用程序用户身份信息的现代化图形界面工具
使用 PyQt5 实现跨平台支持
"""

import os
import sys
import json
import uuid
import shutil
import hashlib
import subprocess
import webbrowser
import platform
import random
import csv
import io
from pathlib import Path
from datetime import datetime, timedelta

try:
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
except ImportError:
    print("错误: 未安装PyQt5")
    print("请运行: pip install PyQt5")
    sys.exit(1)

class CheckedCheckBox(QCheckBox):
    """自定义复选框，确保显示勾勾"""
    def paintEvent(self, event):
        super().paintEvent(event)
        if self.isChecked():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            # 获取indicator的位置和大小
            option = QStyleOptionButton()
            self.initStyleOption(option)
            rect = self.style().subElementRect(QStyle.SE_CheckBoxIndicator, option, self)
            # 绘制白色勾勾
            painter.setPen(QPen(Qt.white, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            check_path = QPainterPath()
            check_path.moveTo(rect.left() + 4, rect.center().y())
            check_path.lineTo(rect.center().x() - 2, rect.bottom() - 4)
            check_path.lineTo(rect.right() - 4, rect.top() + 4)
            painter.drawPath(check_path)

class QoderResetGUI(QMainWindow):
    """Clean-Qoder 主窗口类"""
    VERSION = "1.0"
    
    def __init__(self):
        super().__init__()
        self.current_language = 'zh'  # 默认中文
        self.init_translations()
        self.init_ui()
    
    def init_translations(self):
        """初始化多语言字典"""
        self.translations = {
            'zh': {  # 中文
                'window_title': 'Clean-Qoder',
                'intro_text': 'Clean-Qoder 专业清理工具 - 清理并重置 Qoder 应用的设备标识信息',
                'operation_area': '功能区:',
                'one_click_config': '一键重置配置',
                'close_qoder': '关闭Qoder',
                'reset_machine_id': '重置设备ID',
                'reset_telemetry': '重置遥测信息',
                'deep_identity_clean': '深度清理身份',
                'login_identity_clean': '清理登录信息',
                'hardware_fingerprint_reset': '重置硬件指纹',
                'advanced_options': '高级选项',
                'preserve_chat': '保留聊天记录',
                'operation_log': '运行日志:',
                'clear_log': '清除日志',
                'github': 'Github',
                'language': '语言',
                
                # 日志消息
                'tool_started': 'Clean-Qoder 清理工具已启动',
                'log_cleared': '日志已清除',
                'qoder_running': 'Qoder 正在运行',
                'qoder_not_running': 'Qoder 未运行',
                'qoder_directory_exists': 'Qoder 目录已找到',
                'machine_id': '设备标识',
                'telemetry_machine_id': '遥测标识',
                'device_id': '设备标识',
                'cache_directories_found': '个缓存目录',
                'chat_directories_found': '个聊天相关目录',
                'identity_files_found': '个身份标识文件',
                'status_check_complete': '系统检查完成，准备就绪',
                
                # 对话框消息
                'qoder_detected_running': '检测到 Qoder 正在运行',
                'please_close_qoder': '请手动关闭 Qoder 应用程序',
                'confirm_one_click': '确认执行一键重置',
                'confirm_deep_clean': '确认执行深度清理',
                'confirm_login_clean': '确认清理登录信息',
                'operation_complete': '操作已完成',
                'operation_failed': '操作失败',
                'error': '错误',
                'success': '成功',
                'warning': '警告',
                'status_check': '状态检查',
                
                # 状态检查消息
                'checking_process': '正在检查 Qoder 进程状态',
                'checking_directory': '正在检查 Qoder 目录',
                'checking_machine_id': '正在检查设备标识文件',
                'checking_telemetry': '正在检查遥测数据文件',
                'checking_cache': '正在检查缓存目录',
                'checking_chat': '正在检查聊天记录',
                'checking_identity': '正在检查身份标识文件',
                'checking_shared_cache': '正在检查 SharedClientCache 内部文件',
                'checking_keychain': '正在检查 Keychain 和证书存储',
                'checking_activity': '正在检查用户活动记录',
                'process_running_pid': 'Qoder 正在运行',
                'reading_failed': '读取失败',
                'file_not_exists': '文件不存在',
                'not_found': '未找到',
                'shared_cache_internal': 'SharedClientCache 内部文件',
                'shared_cache_not_exists': 'SharedClientCache 目录不存在',
                'cert_files_found': '个证书/安全文件',
                'activity_files_found': '个活动记录文件',
                'status_check_finished': '状态检查完成，准备就绪',
                'checking_fingerprint': '正在检查设备指纹相关文件',
                'fingerprint_files_found': '个设备指纹文件',
                'qoder_dir_not_exists': 'Qoder 目录不存在',
                'please_install_qoder': '请确保已安装 Qoder 应用程序',
                'status_check_error': '状态检查失败',
                'checking_qoder_status': '正在检查 Qoder 运行状态',
                'qoder_detected_running_pid': '检测到 Qoder 正在运行',
                'please_close_manually': '请手动关闭 Qoder 应用程序',
                'user_cancelled': '用户取消操作',
                'qoder_still_running': 'Qoder 仍在运行，操作取消',
                'please_close_first': '请先完全关闭 Qoder 应用程序',
                'starting_login_cleanup': '开始清理登录相关身份信息',
                'login_cleanup_started': '开始登录身份清理',
                'login_cleanup_completed': '登录身份清理完成',
                'login_cleanup_failed': '登录身份清理失败',
                'can_restart_qoder': '现在可以重新启动 Qoder',
                'confirm_login_cleanup': '确认清理登录身份',
                'starting_deep_cleanup': '开始深度身份清理',
                'starting_reset_machine_id': '开始重置机器ID',
                'machine_id_reset_completed': '机器ID重置完成',
                'starting_reset_telemetry': '开始重置遥测数据',
                'telemetry_reset_completed': '遥测数据重置完成',
                'hardware_fingerprint_completed': '硬件指纹重置完成',
                'suggest_restart_system': '建议重启系统后再使用 Qoder',
                'pid_info_single': '进程ID: {0}',
                'pid_info_multiple': '发现 {0} 个进程',
                'please_close_and_retry': '请先关闭 Qoder 应用程序，然后重试。',
                'please_close_before_continue': '请先关闭 Qoder 后继续操作。'
            },
            'en': {  # English
                'window_title': 'Clean-Qoder',
                'intro_text': 'Clean-Qoder Professional Cleanup Tool - Reset Qoder Application Identity',
                'operation_area': 'Operation Area:',
                'one_click_config': 'One-Click Configuration',
                'close_qoder': 'Close Qoder',
                'reset_machine_id': 'Reset Machine ID',
                'reset_telemetry': 'Reset Telemetry',
                'deep_identity_clean': 'Deep Identity Cleanup',
                'login_identity_clean': 'Clean Login Identity',
                'hardware_fingerprint_reset': 'Hardware Reset',
                'advanced_options': 'Advanced Options',
                'preserve_chat': 'Preserve Chat History',
                'operation_log': 'Operation Log:',
                'clear_log': 'Clear Log',
                'github': 'Github',
                'language': 'Language',
                
                # Log messages
                'tool_started': 'Clean-Qoder professional cleanup tool started',
                'log_cleared': 'Log cleared',
                'qoder_running': 'Qoder is running',
                'qoder_not_running': 'Qoder is not running',
                'qoder_directory_exists': 'Qoder directory exists',
                'machine_id': 'Machine ID',
                'telemetry_machine_id': 'Telemetry Machine ID',
                'device_id': 'Device ID',
                'cache_directories_found': 'cache directories found',
                'chat_directories_found': 'chat-related directories found',
                'identity_files_found': 'identity files found',
                'status_check_complete': 'Status check completed, ready to operate',
                
                # Dialog messages
                'qoder_detected_running': 'Qoder Detected Running',
                'please_close_qoder': 'Please close Qoder application manually',
                'confirm_one_click': 'Confirm One-Click Reset',
                'confirm_deep_clean': 'Confirm Deep Cleanup',
                'confirm_login_clean': 'Confirm Login Identity Cleanup',
                'operation_complete': 'Operation Complete',
                'operation_failed': 'Operation Failed',
                'error': 'Error',
                'success': 'Success',
                'warning': 'Warning',
                'status_check': 'Status Check',
                'pid_info_single': 'Process ID: {0}',
                'pid_info_multiple': 'Found {0} processes',
                'please_close_and_retry': 'Please close Qoder application and try again.',
                'please_close_before_continue': 'Please close Qoder before continuing.'
            },
            'ru': {  # Русский
                'window_title': 'Clean-Qoder',
                'intro_text': 'Clean-Qoder профессиональный инструмент очистки - сброс идентификации приложения Qoder',
                'operation_area': 'Область операций:',
                'one_click_config': 'Одним кликом',
                'close_qoder': 'Закрыть Qoder',
                'reset_machine_id': 'Сбросить ID машины',
                'reset_telemetry': 'Сбросить телеметрию',
                'deep_identity_clean': 'Глубокая очистка',
                'login_identity_clean': 'Очистить вход',
                'hardware_fingerprint_reset': 'Сброс железа',
                'advanced_options': 'Дополнительно',
                'preserve_chat': 'Сохранить чат',
                'operation_log': 'Журнал операций:',
                'clear_log': 'Очистить журнал',
                'github': 'Github',
                'language': 'Язык',

                # Log messages
                'tool_started': 'Профессиональный инструмент очистки Clean-Qoder запущен',
                'log_cleared': 'Журнал очищен',
                'qoder_running': 'Qoder запущен',
                'qoder_not_running': 'Qoder не запущен',
                'qoder_directory_exists': 'Папка Qoder существует',
                'machine_id': 'ID машины',
                'telemetry_machine_id': 'ID машины телеметрии',
                'device_id': 'ID устройства',
                'cache_directories_found': 'папок кеша найдено',
                'chat_directories_found': 'папок чата найдено',
                'identity_files_found': 'файлов идентификации найдено',
                'status_check_complete': 'Проверка статуса завершена, готов к работе',

                # Dialog messages
                'qoder_detected_running': 'Обнаружен запущенный Qoder',
                'please_close_qoder': 'Пожалуйста, закройте приложение Qoder вручную',
                'confirm_one_click': 'Подтвердить сброс одним кликом',
                'confirm_deep_clean': 'Подтвердить глубокую очистку',
                'confirm_login_clean': 'Подтвердить очистку входа',
                'operation_complete': 'Операция завершена',
                'operation_failed': 'Операция не удалась',
                'error': 'Ошибка',
                'success': 'Успех',
                'warning': 'Предупреждение',
                'status_check': 'Проверка статуса',
                'pid_info_single': 'ID процесса: {0}',
                'pid_info_multiple': 'Найдено процессов: {0}',
                'please_close_and_retry': 'Пожалуйста, закройте Qoder и попробуйте снова.',
                'please_close_before_continue': 'Пожалуйста, закройте Qoder перед продолжением.'
            },
            'pt-br': {  # Português (Brasil)
                'window_title': 'Clean-Qoder',
                'intro_text': 'Clean-Qoder Ferramenta de Limpeza Profissional - Redefinir Identidade do Qoder',
                'operation_area': 'Área de Operações:',
                'one_click_config': 'Configuração com um clique',
                'close_qoder': 'Fechar Qoder',
                'reset_machine_id': 'Redefinir ID da Máquina',
                'reset_telemetry': 'Redefinir Telemetria',
                'deep_identity_clean': 'Limpeza Profunda de Identidade',
                'login_identity_clean': 'Limpar Login',
                'hardware_fingerprint_reset': 'Reset de Hardware',
                'advanced_options': 'Opções Avançadas',
                'preserve_chat': 'Preservar Histórico do chat',
                'operation_log': 'Log de Operações:',
                'clear_log': 'Limpar Log',
                'github': 'Github',
                'language': 'Idioma',

                # Log messages
                'tool_started': 'Ferramenta profissional de limpeza Clean-Qoder iniciada',
                'log_cleared': 'Log limpo',
                'qoder_running': 'Qoder está em execução',
                'qoder_not_running': 'Qoder não está em execução',
                'qoder_directory_exists': 'Diretório Qoder existe',
                'machine_id': 'ID da Máquina',
                'telemetry_machine_id': 'ID da Máquina de Telemetria',
                'device_id': 'ID do Dispositivo',
                'cache_directories_found': 'diretórios de cache encontrados',
                'chat_directories_found': 'diretórios relacionados ao chat encontrados',
                'identity_files_found': 'arquivos de identidade encontrados',
                'status_check_complete': 'Verificação de status concluída, pronto para operar',

                # Dialog messages
                'qoder_detected_running': 'Qoder Detectado em Execução',
                'please_close_qoder': 'Por favor, feche o aplicativo Qoder manualmente',
                'confirm_one_click': 'Confirmar Redefinição com um clique',
                'confirm_deep_clean': 'Confirmar Limpeza Profunda',
                'confirm_login_clean': 'Confirmar Limpeza de Identidade de Login',
                'operation_complete': 'Operação Concluída',
                'operation_failed': 'Operação Falhou',
                'error': 'Erro',
                'success': 'Sucesso',
                'warning': 'Aviso',
                'status_check': 'Verificação de Status',
                'pid_info_single': 'ID do Processo: {0}',
                'pid_info_multiple': 'Encontrados {0} processos',
                'please_close_and_retry': 'Por favor, feche o Qoder e tente novamente.',
                'please_close_before_continue': 'Por favor, feche o Qoder antes de continuar.'
            },
            'ja': {  # 日本語
                'window_title': 'Clean-Qoder',
                'intro_text': 'Clean-Qoder プロフェッショナルクリーンツール - QoderアプリケーションのID情報をリセット',
                'operation_area': '操作エリア:',
                'one_click_config': 'ワンクリック設定',
                'close_qoder': 'Qoderを閉じる',
                'reset_machine_id': 'マシンIDをリセット',
                'reset_telemetry': 'テレメトリーをリセット',
                'deep_identity_clean': '深いIDクリーン',
                'login_identity_clean': 'ログインIDをクリーン',
                'hardware_fingerprint_reset': 'ハードウェアリセット',
                'advanced_options': '高度なオプション',
                'preserve_chat': 'チャット履歴を保持',
                'operation_log': '操作ログ:',
                'clear_log': 'ログをクリア',
                'github': 'Github',
                'language': '言語',
                
                # Log messages
                'tool_started': 'Clean-Qoderプロフェッショナルクリーンツールが起動しました',
                'log_cleared': 'ログをクリアしました',
                'qoder_running': 'Qoderが実行中です',
                'qoder_not_running': 'Qoderは実行されていません',
                'qoder_directory_exists': 'Qoderディレクトリが存在します',
                'machine_id': 'マシンID',
                'telemetry_machine_id': 'テレメトリーマシンID',
                'device_id': 'デバイスID',
                'cache_directories_found': 'キャッシュディレクトリが見つかりました',
                'chat_directories_found': 'チャット関連ディレクトリが見つかりました',
                'identity_files_found': 'IDファイルが見つかりました',
                'status_check_complete': 'ステータスチェック完了、操作可能です',
                
                # Dialog messages
                'qoder_detected_running': 'Qoderが実行中です',
                'please_close_qoder': 'Qoderアプリケーションを手動で閉じてください',
                'confirm_one_click': 'ワンクリックリセットを確認',
                'confirm_deep_clean': '深いクリーンを確認',
                'confirm_login_clean': 'ログインIDクリーンを確認',
                'operation_complete': '操作完了',
                'operation_failed': '操作失敗',
                'error': 'エラー',
                'success': '成功',
                'warning': '警告',
                'status_check': 'ステータスチェック',
                'pid_info_single': 'プロセスID: {0}',
                'pid_info_multiple': '{0} 個のプロセスが見つかりました',
                'please_close_and_retry': 'Qoderを閉じてから再度お試しください。',
                'please_close_before_continue': '続行する前にQoderを閉じてください。'
            },
            'ko': {  # 한국어
                'window_title': 'Clean-Qoder',
                'intro_text': 'Clean-Qoder 전문 클린업 도구 - Qoder 애플리케이션 ID 정보 재설정',
                'operation_area': '작업 영역:',
                'one_click_config': '원클릭 설정',
                'close_qoder': 'Qoder 닫기',
                'reset_machine_id': '머신 ID 재설정',
                'reset_telemetry': '원격 측정 재설정',
                'deep_identity_clean': '심층 ID 정리',
                'login_identity_clean': '로그인 ID 정리',
                'hardware_fingerprint_reset': '하드웨어 재설정',
                'advanced_options': '고급 옵션',
                'preserve_chat': '채팅 기록 보존',
                'operation_log': '작업 로그:',
                'clear_log': '로그 지우기',
                'github': 'Github',
                'language': '언어',
                
                # Log messages
                'tool_started': 'Clean-Qoder 전문 클린업 도구가 시작되었습니다',
                'log_cleared': '로그가 지워졌습니다',
                'qoder_running': 'Qoder가 실행 중입니다',
                'qoder_not_running': 'Qoder가 실행되지 않았습니다',
                'qoder_directory_exists': 'Qoder 디렉토리가 존재합니다',
                'machine_id': '머신 ID',
                'telemetry_machine_id': '원격 측정 머신 ID',
                'device_id': '장치 ID',
                'cache_directories_found': '캐시 디렉토리를 찾았습니다',
                'chat_directories_found': '채팅 관련 디렉토리를 찾았습니다',
                'identity_files_found': 'ID 파일을 찾았습니다',
                'status_check_complete': '상태 확인 완료, 작업 가능합니다',
                
                # Dialog messages
                'qoder_detected_running': 'Qoder가 실행 중입니다',
                'please_close_qoder': 'Qoder 애플리케이션을 수동으로 닫아주세요',
                'confirm_one_click': '원클릭 재설정 확인',
                'confirm_deep_clean': '심층 정리 확인',
                'confirm_login_clean': '로그인 ID 정리 확인',
                'operation_complete': '작업 완료',
                'operation_failed': '작업 실패',
                'error': '오류',
                'success': '성공',
                'warning': '경고',
                'status_check': '상태 확인',
                'pid_info_single': '프로세스 ID: {0}',
                'pid_info_multiple': '{0}개의 프로세스를 찾았습니다',
                'please_close_and_retry': 'Qoder를 닫고 다시 시도해주세요.',
                'please_close_before_continue': '계속하기 전에 Qoder를 닫아주세요.'
            }
        }
    
    def tr(self, key):
        """获取当前语言的翻译文本"""
        return self.translations.get(self.current_language, {}).get(key, key)
    
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle(f"{self.tr('window_title')} v{self.VERSION}")
        self.setFixedSize(900, 720)  # 调整为更宽、更矮的窗口
        self.setStyleSheet("""
            background-color: #f5f5f5;
            font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
        """)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 20, 30, 20)
        main_layout.setSpacing(15)
        
        # 添加右上角语言切换组件和GitHub按钮
        top_layout = QHBoxLayout()
        top_layout.addStretch()  # 推到右侧
        
        # 语言标签（增大字体）
        lang_label = QLabel(self.tr('language') + ":")
        lang_label.setStyleSheet("""
            QLabel {
                font-size: 13px;
                color: #666666;
                margin-right: 8px;
            }
        """)
        top_layout.addWidget(lang_label)
        
        # 语言下拉框（下拉菜单样式，增大字体，确保向下展开）
        self.language_combo = QComboBox()
        self.language_combo.addItems(['中文', 'English', 'Русский', 'Português (BR)', '日本語', '한국어'])
        self.language_combo.setFixedSize(130, 32)
        # 确保下拉菜单向下展开
        self.language_combo.setInsertPolicy(QComboBox.NoInsert)
        # 设置下拉列表的最大可见项目数（现在有6种语言）
        self.language_combo.setMaxVisibleItems(6)
        # 设置下拉列表的最小宽度以适应内容
        self.language_combo.setMinimumContentsLength(10)
        # 固定下拉列表的宽度，避免过长
        self.language_combo.setSizeAdjustPolicy(QComboBox.AdjustToContentsOnFirstShow)
        self.language_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 1px solid #dadce0;
                border-radius: 4px;
                padding: 2px 8px;  /* 进一步减少内边距 */
                font-size: 13px;
                color: #333333;
            }
            QComboBox:hover {
                border: 1px solid #4285f4;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;  /* 减少下拉按钮宽度 */
                border-left: 1px solid #dadce0;
                padding-right: 1px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 5px solid #666;
                border-bottom: none;
                width: 0;
                height: 0;
                margin-right: 0px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 1px solid #dadce0;
                selection-background-color: #e8f0fe;
                font-size: 13px;
                padding: 0px;  /* 完全移除内边距 */
                outline: none;
                selection-color: #333333;
                /* 固定宽度以避免过长 */
                min-width: 110px;
                max-width: 150px;
                margin: 0px;  /* 移除外边距 */
                show-decoration-selected: 0;  /* 移除选中装饰 */
            }
            QComboBox::item {
                padding: 2px 8px;  /* 最小垂直内边距 */
                height: 22px;  /* 更小的固定高度 */
                margin: 0px;  /* 移除外边距 */
                border: none;  /* 移除边框 */
            }
            QComboBox::item:selected {
                background-color: #e8f0fe;
                color: #333333;
            }
            QComboBox::item:hover {
                background-color: #f0f0f0;
            }
        """)
        self.language_combo.currentTextChanged.connect(self.change_language)
        
        # 设置下拉列表视图属性，确保紧凑显示
        view = self.language_combo.view()
        view.setTextElideMode(Qt.ElideRight)
        # 设置统一的项目高度
        view.setUniformItemSizes(True)
        # 由于有6个语言选项，允许滚动条
        view.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        # 设置间距为0，确保紧凑显示
        view.setSpacing(0)
        # 设置固定行高，减少间距
        if hasattr(view, 'setRowHeight'):
            view.setRowHeight(0, 24)  # 设置第一行高度，其他行会统一
        # 移除额外的边距
        view.setContentsMargins(0, 0, 0, 0)
        
        top_layout.addWidget(self.language_combo)
        
        # GitHub按钮移到右上角（增大字体）
        self.github_btn = QPushButton('GitHub')
        self.github_btn.setFixedSize(90, 32)
        self.github_btn.setStyleSheet("""
            QPushButton {
                background-color: #2d3748;
                color: white;
                font-size: 13px;
                font-weight: bold;
                border: none;
                border-radius: 4px;
                margin-left: 12px;
            }
            QPushButton:hover {
                background-color: #4a5568;
            }
            QPushButton:pressed {
                background-color: #1a202c;
            }
        """)
        self.github_btn.clicked.connect(self.open_github)
        top_layout.addWidget(self.github_btn)
        
        main_layout.addLayout(top_layout)
        
        # 1. 标题
        self.title_label = QLabel(self.tr('window_title'))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #1a73e8;
                margin-bottom: 5px;
                letter-spacing: 1px;
            }
        """)
        main_layout.addWidget(self.title_label)
        
        # 2. 说明文字（增大字体）
        self.intro_label = QLabel(self.tr('intro_text'))
        self.intro_label.setAlignment(Qt.AlignCenter)
        self.intro_label.setStyleSheet("""
            QLabel {
                font-size: 13px;
                color: #80868b;
                margin-bottom: 15px;
            }
        """)
        main_layout.addWidget(self.intro_label)
        
        # 3. 操作区域标题（增大字体）
        self.operation_title = QLabel(self.tr('operation_area'))
        self.operation_title.setStyleSheet("""
            QLabel {
                font-size: 15px;
                font-weight: bold;
                color: black;
                margin-bottom: 10px;
            }
        """)
        main_layout.addWidget(self.operation_title)
        
        # 4. 蓝色横幅按钮
        self.one_click_btn = QPushButton(self.tr('one_click_config'))
        self.one_click_btn.setFixedSize(320, 45)  # 更宽的按钮
        self.one_click_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4285f4, stop:1 #1967d2);
                color: white;
                font-size: 15px;
                font-weight: bold;
                border: none;
                border-radius: 8px;
                padding: 8px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1967d2, stop:1 #1557b0);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1557b0, stop:1 #0d47a1);
            }
        """)
        self.one_click_btn.clicked.connect(self.one_click_reset)
        
        # 将按钮居中显示
        button_center_layout = QHBoxLayout()
        button_center_layout.addStretch()
        button_center_layout.addWidget(self.one_click_btn)
        button_center_layout.addStretch()
        main_layout.addLayout(button_center_layout)
        
        # 5. 操作按钮网格布局（3x2：三列两行）
        button_layout = QVBoxLayout()
        button_layout.setSpacing(10)
        
        # 第一行按钮（3列）
        button_row1 = QHBoxLayout()
        button_row1.setSpacing(12)
        
        # 关闭Qoder按钮 (红色)
        self.close_qoder_btn = QPushButton(self.tr('close_qoder'))
        self.close_qoder_btn.setFixedSize(170, 42)
        self.close_qoder_btn.setStyleSheet("""
            QPushButton {
                background-color: #ea4335;
                color: white;
                font-size: 13px;
                font-weight: bold;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #d33b2c;
            }
            QPushButton:pressed {
                background-color: #b52d20;
            }
        """)
        self.close_qoder_btn.clicked.connect(self.close_qoder)
        button_row1.addWidget(self.close_qoder_btn)
        
        # 重置机器ID按钮 (蓝色)
        self.reset_machine_id_btn = QPushButton(self.tr('reset_machine_id'))
        self.reset_machine_id_btn.setFixedSize(170, 42)
        self.reset_machine_id_btn.setStyleSheet("""
            QPushButton {
                background-color: #4285f4;
                color: white;
                font-size: 13px;
                font-weight: bold;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #3367d6;
            }
            QPushButton:pressed {
                background-color: #2851a3;
            }
        """)
        self.reset_machine_id_btn.clicked.connect(self.reset_machine_id)
        button_row1.addWidget(self.reset_machine_id_btn)
        
        # 重置遥测数据按钮 (蓝色)
        self.reset_telemetry_btn = QPushButton(self.tr('reset_telemetry'))
        self.reset_telemetry_btn.setFixedSize(170, 42)
        self.reset_telemetry_btn.setStyleSheet("""
            QPushButton {
                background-color: #4285f4;
                color: white;
                font-size: 13px;
                font-weight: bold;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #3367d6;
            }
            QPushButton:pressed {
                background-color: #2851a3;
            }
        """)
        self.reset_telemetry_btn.clicked.connect(self.reset_telemetry)
        button_row1.addWidget(self.reset_telemetry_btn)
        
        button_layout.addLayout(button_row1)
        
        # 第二行按钮（3列）
        button_row2 = QHBoxLayout()
        button_row2.setSpacing(12)
        
        # 深度身份清理按钮 (橙色)
        self.deep_clean_btn = QPushButton(self.tr('deep_identity_clean'))
        self.deep_clean_btn.setFixedSize(170, 42)
        self.deep_clean_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff9800;
                color: white;
                font-size: 13px;
                font-weight: bold;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #f57c00;
            }
            QPushButton:pressed {
                background-color: #e65100;
            }
        """)
        self.deep_clean_btn.clicked.connect(self.deep_identity_cleanup)
        button_row2.addWidget(self.deep_clean_btn)
        
        # 清理登录身份按钮 (紫色)
        self.login_clean_btn = QPushButton(self.tr('login_identity_clean'))
        self.login_clean_btn.setFixedSize(170, 42)
        self.login_clean_btn.setStyleSheet("""
            QPushButton {
                background-color: #673ab7;
                color: white;
                font-size: 13px;
                font-weight: bold;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #5e35b1;
            }
            QPushButton:pressed {
                background-color: #512da8;
            }
        """)
        self.login_clean_btn.clicked.connect(self.login_identity_cleanup)
        button_row2.addWidget(self.login_clean_btn)
        
        # 硬件指纹重置按钮（绿色）
        self.hardware_reset_btn = QPushButton(self.tr('hardware_fingerprint_reset'))
        self.hardware_reset_btn.setFixedSize(170, 42)
        self.hardware_reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #4caf50;
                color: white;
                font-size: 13px;
                font-weight: bold;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        self.hardware_reset_btn.clicked.connect(self.hardware_fingerprint_reset)
        button_row2.addWidget(self.hardware_reset_btn)
        
        button_layout.addLayout(button_row2)
        main_layout.addLayout(button_layout)

        # 5.5. 保留对话记录勾选框（确保显示勾勾）
        self.preserve_chat_checkbox = CheckedCheckBox(self.tr('preserve_chat'))
        self.preserve_chat_checkbox.setChecked(True)  # 默认勾选
        self.preserve_chat_checkbox.setTristate(False)  # 确保只有两种状态
        # 使用样式表，让Qt使用默认的勾勾绘制
        self.preserve_chat_checkbox.setStyleSheet("""
            QCheckBox {
                color: black;
                font-size: 12px;
                font-weight: bold;
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid #4285f4;
                border-radius: 4px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: #4285f4;
                border: 2px solid #4285f4;
            }
            QCheckBox::indicator:checked:hover {
                background-color: #3367d6;
                border: 2px solid #3367d6;
            }
            QCheckBox::indicator:unchecked:hover {
                border: 2px solid #3367d6;
                background-color: #f0f0f0;
            }
        """)

        checkbox_layout = QHBoxLayout()
        checkbox_layout.addWidget(self.preserve_chat_checkbox)
        checkbox_layout.addStretch()
        main_layout.addLayout(checkbox_layout)

        # 6. 操作日志区域（增大字体）
        # 日志标题和清空日志按钮在同一行
        log_header_layout = QHBoxLayout()
        
        self.log_title = QLabel(self.tr('operation_log'))
        self.log_title.setStyleSheet("""
            QLabel {
                font-size: 15px;
                font-weight: bold;
                color: #1a73e8;
                margin-top: 8px;
                margin-bottom: 5px;
            }
        """)
        log_header_layout.addWidget(self.log_title)
        log_header_layout.addStretch()
        
        # 清空日志按钮移到日志框上面（增大字体）
        self.clear_log_btn = QPushButton(self.tr('clear_log'))
        self.clear_log_btn.setFixedSize(90, 32)
        self.clear_log_btn.setStyleSheet("""
            QPushButton {
                background-color: #9aa0a6;
                color: white;
                font-size: 13px;
                font-weight: bold;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #80868b;
            }
            QPushButton:pressed {
                background-color: #5f6368;
            }
        """)
        self.clear_log_btn.clicked.connect(self.clear_log)
        log_header_layout.addWidget(self.clear_log_btn)
        
        main_layout.addLayout(log_header_layout)
        
        # 日志文本框（增大字体）
        self.log_text = QTextEdit()
        self.log_text.setFixedHeight(240)  # 调整日志高度适配新窗口
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #ffffff;
                color: #333333;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                font-size: 11px;
                padding: 12px;
                line-height: 1.6;
            }
        """)
        self.log_text.setReadOnly(True)
        main_layout.addWidget(self.log_text)
        
        # 添加初始日志
        self.log(self.tr('tool_started'))
        self.log("=" * 50)
        self.initialize_status_check()
    
    
    def change_language(self, language_text):
        """切换语言"""
        language_map = {
            '中文': 'zh',
            'English': 'en',
            'Русский': 'ru',
            'Português (BR)': 'pt-br',
            '日本語': 'ja',
            '한국어': 'ko'
        }
        
        new_language = language_map.get(language_text, 'zh')
        if new_language != self.current_language:
            self.current_language = new_language
            self.update_ui_text()
    
    def update_ui_text(self):
        """更新界面文本"""
        # 更新窗口标题
        self.setWindowTitle(f"{self.tr('window_title')} v{self.VERSION}")
        
        # 更新标签文本
        self.title_label.setText(self.tr('window_title'))
        self.intro_label.setText(self.tr('intro_text'))
        self.operation_title.setText(self.tr('operation_area'))
        self.log_title.setText(self.tr('operation_log'))
        
        # 更新按钮文本
        self.one_click_btn.setText(self.tr('one_click_config'))
        self.close_qoder_btn.setText(self.tr('close_qoder'))
        self.reset_machine_id_btn.setText(self.tr('reset_machine_id'))
        self.reset_telemetry_btn.setText(self.tr('reset_telemetry'))
        self.deep_clean_btn.setText(self.tr('deep_identity_clean'))
        self.login_clean_btn.setText(self.tr('login_identity_clean'))
        self.hardware_reset_btn.setText(self.tr('hardware_fingerprint_reset'))
        self.clear_log_btn.setText(self.tr('clear_log'))
        self.github_btn.setText('GitHub')  # GitHub按钮不需要翻译
        
        # 更新复选框文本
        self.preserve_chat_checkbox.setText(self.tr('preserve_chat'))
        
        # 清空日志并重新初始化
        self.log_text.clear()
        self.log(self.tr('tool_started'))
        self.log("=" * 50)
    
    def log(self, message):
        """添加日志消息"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        self.log_text.append(log_message)

        # 自动滚动到最新日志
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def clear_log(self):
        """清空日志"""
        self.log_text.clear()
        self.log(self.tr('log_cleared'))

    def get_qoder_data_dir(self):
        """获取Qoder数据目录路径（跨平台支持）"""
        home_dir = Path.home()
        system = platform.system()

        if system == "Windows":
            # Windows: %APPDATA%\Qoder
            return home_dir / "AppData" / "Roaming" / "Qoder"
        else:
            # 默认使用macOS路径作为fallback
            return home_dir / "Library" / "Application Support" / "Qoder"

    def initialize_status_check(self):
        """初始化时检查各项状态"""
        try:
            # 1. 检查Qoder进程状态
            self.log(f"1. {self.tr('checking_process')}...")
            is_running, pids = self.check_qoder_running()
            if is_running:
                self.log(f"   ✅ {self.tr('process_running_pid')} (PID: {', '.join(pids)})")
            else:
                self.log(f"   ✅ {self.tr('qoder_not_running')}")

            # 2. 检查Qoder目录
            self.log(f"2. {self.tr('checking_directory')}...")
            qoder_support_dir = self.get_qoder_data_dir()

            if qoder_support_dir.exists():
                self.log(f"   ✅ {self.tr('qoder_directory_exists')}")

                # 3. 检查机器ID文件
                self.log(f"3. {self.tr('checking_machine_id')}...")
                machine_id_file = qoder_support_dir / "machineid"
                if machine_id_file.exists():
                    try:
                        with open(machine_id_file, 'r') as f:
                            current_id = f.read().strip()
                        self.log(f"   ✅ {self.tr('machine_id')}: {current_id}")
                    except Exception as e:
                        self.log(f"   ❌ {self.tr('machine_id')} {self.tr('reading_failed')}: {e}")
                else:
                    self.log(f"   ❌ {self.tr('machine_id')} {self.tr('file_not_exists')}")

                # 4. 检查遥测数据文件
                self.log(f"4. {self.tr('checking_telemetry')}...")
                storage_json_file = qoder_support_dir / "User/globalStorage/storage.json"
                if storage_json_file.exists():
                    try:
                        with open(storage_json_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)

                        if 'telemetry.machineId' in data:
                            machine_id = data['telemetry.machineId']
                            self.log(f"   ✅ {self.tr('telemetry_machine_id')}: {machine_id[:16]}...")
                        else:
                            self.log(f"   ⚠️  {self.tr('telemetry_machine_id')} {self.tr('not_found')}")

                        if 'telemetry.devDeviceId' in data:
                            device_id = data['telemetry.devDeviceId']
                            self.log(f"   ✅ {self.tr('device_id')}: {device_id}")
                        else:
                            self.log(f"   ⚠️  {self.tr('device_id')} {self.tr('not_found')}")

                    except Exception as e:
                        self.log(f"   ❌ {self.tr('checking_telemetry')} {self.tr('reading_failed')}: {e}")
                else:
                    self.log(f"   ❌ {self.tr('checking_telemetry')} {self.tr('file_not_exists')}")

                # 5. 检查缓存目录
                self.log(f"5. {self.tr('checking_cache')}...")
                cache_dirs = [
                    "Cache", "blob_storage", "Code Cache", "SharedClientCache",
                    "GPUCache", "DawnGraphiteCache", "DawnWebGPUCache"
                ]

                cache_count = 0
                for cache_dir in cache_dirs:
                    cache_path = qoder_support_dir / cache_dir
                    if cache_path.exists():
                        cache_count += 1

                self.log(f"   ✅ 发现 {cache_count}/{len(cache_dirs)} {self.tr('cache_directories_found')}")

                # 6. 检查对话记录相关目录
                self.log(f"6. {self.tr('checking_chat')}...")
                chat_dirs = [
                    "User/workspaceStorage", "User/History", "logs", "CachedData"
                ]

                chat_count = 0
                for chat_dir in chat_dirs:
                    chat_path = qoder_support_dir / chat_dir
                    if chat_path.exists():
                        chat_count += 1

                self.log(f"   ✅ 发现 {chat_count}/{len(chat_dirs)} {self.tr('chat_directories_found')}")
                
                # 7. 检查身份识别文件
                self.log(f"7. {self.tr('checking_identity')}...")
                identity_files = [
                    "Network Persistent State", "Cookies", "SharedStorage", 
                    "Trust Tokens", "TransportSecurity", "Preferences"
                ]
                
                identity_count = 0
                for identity_file in identity_files:
                    file_path = qoder_support_dir / identity_file
                    if file_path.exists():
                        identity_count += 1
                
                self.log(f"   ✅ 发现 {identity_count}/{len(identity_files)} {self.tr('identity_files_found')}")
                
                # 8. 检查 SharedClientCache 内部文件
                self.log(f"8. {self.tr('checking_shared_cache')}...")
                shared_cache = qoder_support_dir / "SharedClientCache"
                if shared_cache.exists():
                    critical_files = [".info", ".lock", "mcp.json"]
                    shared_count = 0
                    for file_name in critical_files:
                        if (shared_cache / file_name).exists():
                            shared_count += 1
                    
                    # 检查 index 目录
                    if (shared_cache / "index").exists():
                        shared_count += 1
                    
                    self.log(f"   ✅ {self.tr('shared_cache_internal')}: {shared_count}/4 个")
                else:
                    self.log(f"   ⚠️  {self.tr('shared_cache_not_exists')}")
                
                # 9. 检查 Keychain 和证书存储
                self.log(f"9. {self.tr('checking_keychain')}...")
                keychain_files = [
                    "cert_transparency_reporter_state.json",
                    "Certificate Revocation Lists",
                    "SSLCertificates"
                ]
                
                keychain_count = 0
                for keychain_file in keychain_files:
                    file_path = qoder_support_dir / keychain_file
                    if file_path.exists():
                        keychain_count += 1
                
                self.log(f"   ✅ 发现 {keychain_count}/{len(keychain_files)} {self.tr('cert_files_found')}")
                
                # 10. 检查用户活动记录
                self.log(f"10. {self.tr('checking_activity')}...")
                activity_files = [
                    "ActivityLog", "EventLog", "UserActivityLog",
                    "Login Credentials", "Web Data", "Web Data-journal"
                ]
                
                activity_count = 0
                for activity_file in activity_files:
                    file_path = qoder_support_dir / activity_file
                    if file_path.exists():
                        activity_count += 1
                
                self.log(f"   ✅ 发现 {activity_count}/{len(activity_files)} 个活动记录文件")
                
                # 11. 检查设备指纹相关文件
                self.log(f"11. {self.tr('checking_fingerprint')}...")
                fingerprint_files = [
                    "DeviceMetadata", "HardwareInfo", "SystemInfo",
                    "QuotaManager", "QuotaManager-journal",
                    "databases/Databases.db", "databases/Databases.db-journal"
                ]
                
                fingerprint_count = 0
                for fingerprint_file in fingerprint_files:
                    file_path = qoder_support_dir / fingerprint_file
                    if file_path.exists():
                        fingerprint_count += 1
                
                self.log(f"   ✅ 发现 {fingerprint_count}/{len(fingerprint_files)} {self.tr('fingerprint_files_found')}")

            else:
                self.log(f"   ❌ {self.tr('qoder_dir_not_exists')}")
                self.log(f"   {self.tr('please_install_qoder')}")

            self.log("=" * 50)
            self.log(self.tr('status_check_finished'))

        except Exception as e:
            self.log(f"❌ {self.tr('status_check_error')}: {e}")
            self.log("=" * 50)
    
    def check_qoder_running(self):
        """检查Qoder是否正在运行（跨平台支持，精确匹配）"""
        system = platform.system()
        pids = []
        
        # Qoder进程名的可能变体（精确匹配）
        qoder_names = ['qoder.exe', 'qoder', 'qoder.exe', 'qoder-app.exe']
        
        try:
            if system == "Windows":
                # Windows: 精确匹配Qoder进程名
                try:
                    # 方法1: 使用tasklist /FI过滤，只查找Qoder进程
                    result = subprocess.run(
                        ['tasklist', '/FI', 'IMAGENAME eq Qoder.exe', '/FO', 'CSV', '/NH'],
                        capture_output=True,
                        text=True,
                        creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0,
                        timeout=10
                    )
                    
                    # 如果没找到，尝试其他可能的进程名
                    if result.returncode != 0 or not result.stdout.strip():
                        for qoder_name in qoder_names:
                            result = subprocess.run(
                                ['tasklist', '/FI', f'IMAGENAME eq {qoder_name}', '/FO', 'CSV', '/NH'],
                                capture_output=True,
                                text=True,
                                creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0,
                                timeout=10
                            )
                            if result.returncode == 0 and result.stdout.strip():
                                break
                    
                    # 解析CSV格式的输出（只处理实际匹配的进程）
                    if result.returncode == 0:
                        for line in result.stdout.split('\n'):
                            line = line.strip()
                            if not line:
                                continue
                            # CSV格式: "进程名","PID","会话名","会话#","内存使用"
                            try:
                                reader = csv.reader(io.StringIO(line))
                                row = next(reader)
                                if len(row) >= 2:
                                    proc_name = row[0].strip('"').lower()
                                    pid = row[1].strip('"')
                                    # 精确匹配进程名（不区分大小写）
                                    if proc_name in [name.lower() for name in qoder_names] and pid.isdigit():
                                        pids.append(pid)
                            except Exception:
                                continue
                    
                    # 方法2: 使用wmic作为备用方法（精确匹配）
                    if not pids:
                        for qoder_name in qoder_names:
                            result = subprocess.run(
                                ['wmic', 'process', 'where', f'name="{qoder_name}"', 'get', 'ProcessId', '/format:value'],
                                capture_output=True,
                                text=True,
                                creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0,
                                timeout=10
                            )
                            if result.returncode == 0:
                                for line in result.stdout.split('\n'):
                                    line = line.strip()
                                    if line.startswith('ProcessId='):
                                        pid = line.split('=')[1].strip()
                                        if pid.isdigit():
                                            pids.append(pid)
                            if pids:
                                break
                    
                except Exception:
                    pass
                
                # Windows方法3: 如果以上方法都失败，尝试使用psutil（精确匹配）
                if not pids:
                    try:
                        import psutil
                        for proc in psutil.process_iter(['pid', 'name', 'exe']):
                            try:
                                proc_name = proc.info['name'] or ''
                                proc_exe = proc.info.get('exe', '') or ''
                                proc_name_lower = proc_name.lower()
                                
                                # 精确匹配进程名
                                if any(qoder_name.lower() == proc_name_lower for qoder_name in qoder_names):
                                    pids.append(str(proc.info['pid']))
                                # 或者检查可执行文件路径
                                elif proc_exe and any(qoder_name.lower() in proc_exe.lower() for qoder_name in qoder_names):
                                    # 进一步验证：确保路径中包含Qoder（排除其他包含该字符串的进程）
                                    if 'qoder' in proc_exe.lower().replace('\\', '/').split('/')[-1]:
                                        pids.append(str(proc.info['pid']))
                            except (psutil.NoSuchProcess, psutil.AccessDenied, KeyError):
                                pass
                    except ImportError:
                        pass
                
            else:
                # Linux/macOS: 使用pgrep命令（精确匹配进程名）
                try:
                    # 先尝试精确匹配进程名
                    result = subprocess.run(
                        ['pgrep', '-x', 'Qoder'],
                        capture_output=True,
                        text=True
                    )
                    if result.returncode == 0:
                        pids = [pid.strip() for pid in result.stdout.strip().split('\n') if pid.strip()]
                    else:
                        # 如果精确匹配失败，尝试模糊匹配（但限制为包含Qoder的进程）
                        result = subprocess.run(
                            ['pgrep', '-f', 'Qoder'],
                            capture_output=True,
                            text=True
                        )
                        if result.returncode == 0:
                            # 进一步验证：检查进程命令行是否真的包含Qoder
                            all_pids = [pid.strip() for pid in result.stdout.strip().split('\n') if pid.strip()]
                            for pid in all_pids:
                                try:
                                    # 获取进程命令行
                                    cmd_result = subprocess.run(
                                        ['ps', '-p', pid, '-o', 'comm='],
                                        capture_output=True,
                                        text=True,
                                        timeout=5
                                    )
                                    if cmd_result.returncode == 0 and 'Qoder' in cmd_result.stdout:
                                        pids.append(pid)
                                except Exception:
                                    # 如果验证失败，仍然添加（可能是权限问题）
                                    pids.append(pid)
                except Exception:
                    pass
            
            # 去重并清理空字符串
            pids = list(set([pid for pid in pids if pid]))
            
            if pids:
                return True, pids
                
        except Exception as e:
            # 静默处理异常
            pass
        
        return False, []

    def generate_system_version(self, system_type):
        """根据系统类型生成合适的系统版本号"""
        if system_type == "Darwin":  # macOS
            # macOS 版本号格式: 14.x.x (Sonoma), 13.x.x (Ventura), 12.x.x (Monterey)
            major_versions = [12, 13, 14, 15]  # 支持新版本
            major = random.choice(major_versions)
            minor = random.randint(0, 6)
            patch = random.randint(0, 9)
            return f"{major}.{minor}.{patch}"
        elif system_type == "Windows":
            # Windows 10/11 版本号
            versions = [
                "10.0.19045",  # Windows 10 22H2
                "10.0.22621",  # Windows 11 22H2
                "10.0.22631",  # Windows 11 23H2
                "10.0.26100"   # Windows 11 24H2
            ]
            base_version = random.choice(versions)
            # 添加随机的小版本号
            build_suffix = random.randint(1, 999)
            return f"{base_version}.{build_suffix}"
        else:  # Linux 或其他系统
            # Linux 内核版本号格式: 5.x.x, 6.x.x
            major_versions = [5, 6]
            major = random.choice(major_versions)
            if major == 5:
                minor = random.randint(10, 19)  # 5.10-5.19
            else:  # major == 6
                minor = random.randint(0, 8)    # 6.0-6.8
            patch = random.randint(0, 50)
            return f"{major}.{minor}.{patch}"

    def terminate_qoder_process(self, pids):
        """终止Qoder进程（跨平台支持，多种方法）"""
        system = platform.system()
        terminated_count = 0
        import time
        
        try:
            if system == "Windows":
                # Windows: 使用多种方法确保进程被终止
                for pid in pids:
                    success = False
                    pid_int = int(pid) if pid.isdigit() else None
                    
                    if pid_int is None:
                        self.log(f"   ⚠️  无效的 PID: {pid}")
                        continue
                    
                    # 方法1: 使用taskkill /F (强制终止)
                    try:
                        result = subprocess.run(
                            ['taskkill', '/PID', pid, '/F', '/T'],
                            capture_output=True,
                            text=True,
                            creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0,
                            timeout=5
                        )
                        if result.returncode == 0 or '成功' in result.stdout or 'successfully' in result.stdout.lower():
                            terminated_count += 1
                            success = True
                            self.log(f"   ✅ 已终止进程 PID: {pid} (taskkill)")
                        else:
                            self.log(f"   ⚠️  taskkill 失败 PID: {pid} - {result.stdout[:100]}")
                    except Exception as e:
                        self.log(f"   ⚠️  taskkill 出错 PID: {pid}: {str(e)[:100]}")
                    
                    # 方法2: 如果taskkill失败，使用wmic
                    if not success:
                        try:
                            result = subprocess.run(
                                ['wmic', 'process', 'where', f'ProcessId={pid_int}', 'delete'],
                                capture_output=True,
                                text=True,
                                creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0,
                                timeout=5
                            )
                            if result.returncode == 0:
                                terminated_count += 1
                                success = True
                                self.log(f"   ✅ 已终止进程 PID: {pid} (wmic)")
                        except Exception as e:
                            self.log(f"   ⚠️  wmic 出错 PID: {pid}: {str(e)[:100]}")
                    
                    # 方法3: 如果以上都失败，尝试使用psutil (如果可用)
                    if not success:
                        try:
                            import psutil
                            proc = psutil.Process(pid_int)
                            proc.kill()
                            terminated_count += 1
                            success = True
                            self.log(f"   ✅ 已终止进程 PID: {pid} (psutil)")
                        except (ImportError, psutil.NoSuchProcess, psutil.AccessDenied) as e:
                            self.log(f"   ⚠️  psutil 失败 PID: {pid}: {str(type(e).__name__)}")
                    
                    if not success:
                        self.log(f"   ❌ 无法终止进程 PID: {pid}")
                    
            else:
                # macOS/Linux: 使用kill命令（多种信号）
                for pid in pids:
                    success = False
                    pid_int = int(pid) if pid.isdigit() else None
                    
                    if pid_int is None:
                        self.log(f"   ⚠️  无效的 PID: {pid}")
                        continue
                    
                    # 方法1: 先尝试 SIGTERM (正常终止)
                    try:
                        result = subprocess.run(
                            ['kill', '-15', pid],
                            capture_output=True,
                            text=True,
                            timeout=3
                        )
                        if result.returncode == 0:
                            time.sleep(0.5)
                            # 检查是否已终止
                            check_result = subprocess.run(
                                ['kill', '-0', pid],
                                capture_output=True,
                                text=True
                            )
                            if check_result.returncode != 0:
                                terminated_count += 1
                                success = True
                                self.log(f"   ✅ 已终止进程 PID: {pid} (SIGTERM)")
                    except Exception:
                        pass
                    
                    # 方法2: 如果SIGTERM失败，使用SIGKILL (强制终止)
                    if not success:
                        try:
                            result = subprocess.run(
                                ['kill', '-9', pid],
                                capture_output=True,
                                text=True,
                                timeout=3
                            )
                            if result.returncode == 0:
                                terminated_count += 1
                                success = True
                                self.log(f"   ✅ 已终止进程 PID: {pid} (SIGKILL)")
                            else:
                                self.log(f"   ⚠️  kill -9 失败 PID: {pid}")
                        except Exception as e:
                            self.log(f"   ⚠️  kill 出错 PID: {pid}: {str(e)[:100]}")
                    
                    # 方法3: 尝试使用psutil
                    if not success:
                        try:
                            import psutil
                            proc = psutil.Process(pid_int)
                            proc.kill()
                            terminated_count += 1
                            success = True
                            self.log(f"   ✅ 已终止进程 PID: {pid} (psutil)")
                        except (ImportError, psutil.NoSuchProcess, psutil.AccessDenied):
                            pass
                    
                    if not success:
                        self.log(f"   ❌ 无法终止进程 PID: {pid}")
            
            # 等待进程完全结束
            time.sleep(1.5)
            
            # 验证进程是否已关闭
            is_still_running, remaining_pids = self.check_qoder_running()
            if is_still_running:
                self.log(f"   ⚠️  仍有 {len(remaining_pids)} 个进程未关闭")
                return False, terminated_count
            else:
                return True, terminated_count
                
        except Exception as e:
            self.log(f"   ❌ 终止进程时出错: {str(e)[:200]}")
            return False, terminated_count

    def close_qoder(self):
        """关闭Qoder"""
        self.log(self.tr('checking_qoder_status') + "...")

        is_running, pids = self.check_qoder_running()

        if is_running:
            self.log(f"{self.tr('qoder_detected_running_pid')} (PID: {', '.join(pids)})")
            self.log(self.tr('please_close_manually'))
            
            # 简化提示信息，只显示关键内容
            if len(pids) == 1:
                pid_info = self.tr('pid_info_single').format(pids[0])
            else:
                pid_info = self.tr('pid_info_multiple').format(len(pids))
            
            QMessageBox.information(
                self, 
                self.tr('qoder_detected_running'),
                f"{self.tr('qoder_detected_running')}\n\n{pid_info}\n\n{self.tr('please_close_and_retry')}"
            )
        else:
            self.log(self.tr('qoder_not_running'))
            QMessageBox.information(self, self.tr('status_check'), self.tr('qoder_not_running'))

    def login_identity_cleanup(self):
        """专门清理登录相关身份信息"""
        self.log(self.tr('starting_login_cleanup') + "...")

        # 检查Qoder是否在运行
        is_running, pids = self.check_qoder_running()
        if is_running:
            pid_info = self.tr('pid_info_single').format(pids[0]) if len(pids) == 1 else self.tr('pid_info_multiple').format(len(pids))
            reply = QMessageBox.question(self, self.tr('qoder_detected_running'),
                                       f"{self.tr('qoder_detected_running')}\n{pid_info}\n\n{self.tr('please_close_before_continue')}",
                                       QMessageBox.Yes | QMessageBox.No)
            if reply != QMessageBox.Yes:
                self.log(self.tr('user_cancelled'))
                return

            # 再次检查
            is_running, _ = self.check_qoder_running()
            if is_running:
                self.log(self.tr('qoder_still_running'))
                QMessageBox.critical(self, self.tr('error'), self.tr('please_close_first'))
                return

        # 确认操作
        reply = QMessageBox.question(self, self.tr('confirm_login_cleanup'),
                                   f"登录身份清理将：\n\n"
                                   f"• 清除所有登录证书和 Cookies\n"
                                   f"• 清除 SharedClientCache 登录状态\n"
                                   f"• 清除网络状态和会话存储\n"
                                   f"• 清除设备认证信息\n"
                                   f"• 清除 nonce 和 challenge 相关数据\n\n"
                                   f"这将使 Qoder 无法识别之前的登录状态，确定继续吗？",
                                   QMessageBox.Yes | QMessageBox.No)
        if reply != QMessageBox.Yes:
            self.log(self.tr('user_cancelled'))
            return

        try:
            qoder_support_dir = self.get_qoder_data_dir()
            
            if not qoder_support_dir.exists():
                raise Exception("未找到 Qoder 应用数据目录")
            
            self.log("=" * 40)
            self.log(self.tr('login_cleanup_started'))
            self.log("=" * 40)
            
            # 执行登录身份清理
            self.perform_login_identity_cleanup(qoder_support_dir)
            
            self.log("=" * 40)
            self.log(self.tr('login_cleanup_completed') + "！")
            self.log("=" * 40)
            
            QMessageBox.information(self, self.tr('operation_complete'), self.tr('login_cleanup_completed') + "！\n" + self.tr('can_restart_qoder') + "。")
            
        except Exception as e:
            self.log(f"{self.tr('login_cleanup_failed')}: {e}")
            QMessageBox.critical(self, self.tr('error'), f"{self.tr('login_cleanup_failed')}: {e}")
    
    def perform_login_identity_cleanup(self, qoder_support_dir):
        """执行登录相关身份清理"""
        try:
            self.log(self.tr('starting_login_cleanup') + "...")
            cleaned_count = 0
            
            # 1. 清理 SharedClientCache 中的登录状态文件
            self.log("1. 清理 SharedClientCache 登录状态...")
            shared_cache = qoder_support_dir / "SharedClientCache"
            if shared_cache.exists():
                # 清理关键的登录相关文件
                login_files = [".info", ".lock", "mcp.json", "server.json", "auth.json"]
                for file_name in login_files:
                    file_path = shared_cache / file_name
                    if file_path.exists():
                        try:
                            file_path.unlink()
                            self.log(f"   已清除: SharedClientCache/{file_name}")
                            cleaned_count += 1
                        except Exception as e:
                            self.log(f"   清除失败 {file_name}: {e}")
                
                # 清理所有临时文件
                import glob
                temp_pattern = str(shared_cache / "tmp*")
                temp_files = glob.glob(temp_pattern)
                for temp_file in temp_files:
                    try:
                        Path(temp_file).unlink()
                        self.log(f"   已清除: {Path(temp_file).name}")
                        cleaned_count += 1
                    except Exception as e:
                        self.log(f"   清除失败 {Path(temp_file).name}: {e}")
            
            # 2. 清理登录证书和认证文件
            self.log("2. 清理登录证书和认证文件...")
            auth_files = [
                "Login Credentials", "Login Data", "Login Data-journal",
                "Cookies", "Cookies-journal",
                "Network Persistent State",
                "cert_transparency_reporter_state.json",
                "TransportSecurity",
                "Trust Tokens", "Trust Tokens-journal"
            ]
            
            for auth_file in auth_files:
                file_path = qoder_support_dir / auth_file
                if file_path.exists():
                    try:
                        file_path.unlink()
                        self.log(f"   已清除: {auth_file}")
                        cleaned_count += 1
                    except Exception as e:
                        self.log(f"   清除失败 {auth_file}: {e}")
            
            # 3. 清理会话和状态存储
            self.log("3. 清理会话和状态存储...")
            session_dirs = [
                "Session Storage",
                "Local Storage",
                "WebStorage",
                "SharedStorage",
                "Shared Dictionary"
            ]
            
            for session_dir in session_dirs:
                dir_path = qoder_support_dir / session_dir
                if dir_path.exists():
                    try:
                        shutil.rmtree(dir_path)
                        self.log(f"   已清除: {session_dir}")
                        cleaned_count += 1
                    except Exception as e:
                        self.log(f"   清除失败 {session_dir}: {e}")
            
            # 4. 清理用户配置中的登录相关信息
            self.log("4. 清理用户配置中的登录信息...")
            storage_json_file = qoder_support_dir / "User/globalStorage/storage.json"
            if storage_json_file.exists():
                try:
                    with open(storage_json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # 清除登录相关的配置键
                    login_keys = []
                    for key in data.keys():
                        if any(keyword in key.lower() for keyword in [
                            'login', 'auth', 'token', 'credential', 'session',
                            'nonce', 'challenge', 'device', 'account', 'user'
                        ]):
                            login_keys.append(key)
                    
                    if login_keys:
                        for key in login_keys:
                            del data[key]
                            self.log(f"   已清除配置: {key}")
                        
                        with open(storage_json_file, 'w', encoding='utf-8') as f:
                            json.dump(data, f, indent=4, ensure_ascii=False)
                        
                        cleaned_count += len(login_keys)
                        self.log(f"   已清除 {len(login_keys)} 个登录相关配置")
                    else:
                        self.log("   未找到登录相关配置")
                
                except Exception as e:
                    self.log(f"   清理用户配置失败: {e}")
            
            # 5. 清理设备指纹和认证数据
            self.log("5. 清理设备指纹和认证数据...")
            device_files = [
                "DeviceMetadata", "HardwareInfo", "SystemInfo",
                "origin_bound_certs", "AutofillStrikeDatabase",
                "AutofillStrikeDatabase-journal", "Feature Engagement Tracker"
            ]
            
            for device_file in device_files:
                file_path = qoder_support_dir / device_file
                if file_path.exists():
                    try:
                        if file_path.is_dir():
                            shutil.rmtree(file_path)
                        else:
                            file_path.unlink()
                        self.log(f"   已清除: {device_file}")
                        cleaned_count += 1
                    except Exception as e:
                        self.log(f"   清除失败 {device_file}: {e}")
            
            self.log(f"   {self.tr('login_cleanup_completed')}，处理了 {cleaned_count} 个项目")
            
        except Exception as e:
            self.log(f"   {self.tr('login_cleanup_failed')}: {e}")

    def deep_identity_cleanup(self):
        """深度身份清理功能"""
        self.log(self.tr('starting_deep_cleanup') + "...")

        # 检查Qoder是否在运行
        is_running, pids = self.check_qoder_running()
        if is_running:
            pid_info = self.tr('pid_info_single').format(pids[0]) if len(pids) == 1 else self.tr('pid_info_multiple').format(len(pids))
            reply = QMessageBox.question(self, self.tr('qoder_detected_running'),
                                       f"{self.tr('qoder_detected_running')}\n{pid_info}\n\n{self.tr('please_close_before_continue')}",
                                       QMessageBox.Yes | QMessageBox.No)
            if reply != QMessageBox.Yes:
                self.log("用户取消操作")
                return

            # 再次检查
            is_running, _ = self.check_qoder_running()
            if is_running:
                self.log("Qoder 仍在运行，操作取消")
                QMessageBox.critical(self, "错误", "请先完全关闭 Qoder 应用程序")
                return

        # 确认操作
        reply = QMessageBox.question(self, "确认深度清理",
                                   f"深度身份清理将：\n\n"
                                   f"• 清除所有网络状态和 Cookie\n"
                                   f"• 清除所有本地存储数据\n"
                                   f"• 清除 SharedClientCache 内部文件\n"
                                   f"• 清除系统级别身份文件\n"
                                   f"• 清除崩溃报告和缓存数据\n\n"
                                   f"这是最强力的身份重置，确定继续吗？",
                                   QMessageBox.Yes | QMessageBox.No)
        if reply != QMessageBox.Yes:
            self.log("用户取消深度清理")
            return

        try:
            qoder_support_dir = self.get_qoder_data_dir()
            
            if not qoder_support_dir.exists():
                raise Exception("未找到 Qoder 应用数据目录")
            
            self.log("=" * 40)
            self.log("开始深度身份清理")
            self.log("=" * 40)
            
            # 执行高级身份清理
            self.perform_advanced_identity_cleanup(qoder_support_dir, preserve_chat=False)
            
            # 执行超级深度清理（新增增强功能）
            self.log("执行超级深度清理...")
            self.perform_super_deep_cleanup(qoder_support_dir)
            
            self.log("=" * 40)
            self.log("深度身份清理完成！")
            self.log("=" * 40)
            
            QMessageBox.information(self, "完成", "深度身份清理完成！\n现在可以重新启动 Qoder。")
            
        except Exception as e:
            self.log(f"深度清理失败: {e}")
            QMessageBox.critical(self, "错误", f"深度清理失败: {e}")

    def reset_machine_id(self):
        """重置机器ID（增强版）"""
        self.log(self.tr('starting_reset_machine_id') + "...")

        # 检查Qoder是否在运行
        is_running, pids = self.check_qoder_running()
        if is_running:
            pid_info = self.tr('pid_info_single').format(pids[0]) if len(pids) == 1 else self.tr('pid_info_multiple').format(len(pids))
            QMessageBox.critical(self, self.tr('error'), 
                                f"{self.tr('qoder_detected_running')}\n{pid_info}\n\n{self.tr('please_close_before_continue')}")
            return

        try:
            qoder_support_dir = self.get_qoder_data_dir()

            if not qoder_support_dir.exists():
                raise Exception("未找到 Qoder 应用数据目录")

            # 1. 重置主机器ID文件
            machine_id_file = qoder_support_dir / "machineid"
            new_machine_id = str(uuid.uuid4())
            with open(machine_id_file, 'w') as f:
                f.write(new_machine_id)
            self.log(f"主机器ID已重置为: {new_machine_id}")
            
            # 2. 创建多个可能的机器ID文件（增强防检测）
            additional_id_files = [
                "deviceid", "hardware_uuid", "system_uuid", 
                "platform_id", "installation_id"
            ]
            for id_file in additional_id_files:
                file_path = qoder_support_dir / id_file
                new_id = str(uuid.uuid4())
                with open(file_path, 'w') as f:
                    f.write(new_id)
                self.log(f"已创建: {id_file}")
            
            # 3. 同时重置 storage.json 中的机器ID
            storage_json_file = qoder_support_dir / "User/globalStorage/storage.json"
            if storage_json_file.exists():
                with open(storage_json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                machine_id_hash = hashlib.sha256(new_machine_id.encode()).hexdigest()
                data['telemetry.machineId'] = machine_id_hash
                data['machineId'] = machine_id_hash
                
                with open(storage_json_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                
                self.log(f"遥测机器ID: {machine_id_hash[:16]}...")
            
            QMessageBox.information(self, self.tr('success'), self.tr('machine_id_reset_completed'))

        except Exception as e:
            self.log(f"重置机器ID失败: {e}")
            QMessageBox.critical(self, "错误", f"重置机器ID失败: {e}")

    def reset_telemetry(self):
        """重置遥测数据"""
        self.log(self.tr('starting_reset_telemetry') + "...")

        # 检查Qoder是否在运行
        is_running, pids = self.check_qoder_running()
        if is_running:
            pid_info = self.tr('pid_info_single').format(pids[0]) if len(pids) == 1 else self.tr('pid_info_multiple').format(len(pids))
            QMessageBox.critical(self, self.tr('error'), 
                                f"{self.tr('qoder_detected_running')}\n{pid_info}\n\n{self.tr('please_close_before_continue')}")
            return

        try:
            qoder_support_dir = self.get_qoder_data_dir()
            storage_json_file = qoder_support_dir / "User/globalStorage/storage.json"

            if not storage_json_file.exists():
                raise Exception("未找到遥测数据文件")

            with open(storage_json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 生成新的遥测ID
            new_uuid = str(uuid.uuid4())
            machine_id_hash = hashlib.sha256(new_uuid.encode()).hexdigest()
            device_id = str(uuid.uuid4())

            data['telemetry.machineId'] = machine_id_hash
            data['telemetry.devDeviceId'] = device_id

            with open(storage_json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            self.log("遥测数据已重置")
            self.log(f"新遥测机器ID: {machine_id_hash[:16]}...")
            self.log(f"新设备ID: {device_id}")
            QMessageBox.information(self, self.tr('success'), self.tr('telemetry_reset_completed'))

        except Exception as e:
            self.log(f"重置遥测数据失败: {e}")
            QMessageBox.critical(self, "错误", f"重置遥测数据失败: {e}")

    def one_click_reset(self):
        """一键修改所有配置"""
        self.log("开始一键修改所有配置...")

        # 检查Qoder是否在运行
        is_running, pids = self.check_qoder_running()
        if is_running:
            pid_info = self.tr('pid_info_single').format(pids[0]) if len(pids) == 1 else self.tr('pid_info_multiple').format(len(pids))
            reply = QMessageBox.question(self, self.tr('qoder_detected_running'),
                                       f"{self.tr('qoder_detected_running')}\n{pid_info}\n\n{self.tr('please_close_before_continue')}",
                                       QMessageBox.Yes | QMessageBox.No)
            if reply != QMessageBox.Yes:
                self.log("用户取消操作")
                return

            # 再次检查
            is_running, _ = self.check_qoder_running()
            if is_running:
                self.log("Qoder 仍在运行，操作取消")
                QMessageBox.critical(self, "错误", "请先完全关闭 Qoder 应用程序")
                return

        # 确认操作
        preserve_chat = self.preserve_chat_checkbox.isChecked()
        chat_action = "保留对话记录" if preserve_chat else "清除对话记录"

        reply = QMessageBox.question(self, "确认一键修改",
                                   f"一键修改所有配置将：\n\n"
                                   f"• 重置机器ID\n"
                                   f"• 重置遥测数据\n"
                                   f"• 清理缓存数据\n"
                                   f"• 清理身份识别文件 (Cookies, 网络状态等)\n"
                                   f"• 执行高级身份清理 (SharedClientCache 等)\n"
                                   f"• 登录身份清理 (清除认证令牌、登录状态)\n"
                                   f"• 硬件指纹重置 (生成虚假硬件信息)\n"
                                   f"• 超级深度清理 (系统级缓存、网络痕迹、指纹混淆)\n"
                                   f"• {chat_action}\n\n"
                                   f"这是最全面的反检测重置方案（9项功能），确定继续吗？",
                                   QMessageBox.Yes | QMessageBox.No)
        if reply != QMessageBox.Yes:
            self.log("用户取消一键修改")
            return

        try:
            self.log("=" * 40)
            self.log("开始一键修改所有配置")
            self.log("=" * 40)

            # 执行重置操作
            preserve_chat = self.preserve_chat_checkbox.isChecked()
            self.perform_full_reset(preserve_chat)

            self.log("=" * 40)
            self.log("一键修改完成！")
            self.log("=" * 40)

            QMessageBox.information(self, "完成", "一键修改所有配置完成！\n现在可以重新启动 Qoder。")

        except Exception as e:
            self.log(f"一键修改失败: {e}")
            QMessageBox.critical(self, "错误", f"一键修改失败: {e}")

    def perform_full_reset(self, preserve_chat=True):
        """执行完整重置"""
        qoder_support_dir = self.get_qoder_data_dir()

        if not qoder_support_dir.exists():
            raise Exception("未找到 Qoder 应用数据目录")

        # 1. 重置机器ID（增强版）
        self.log("1. 重置机器ID...")
        # 主机器ID文件
        machine_id_file = qoder_support_dir / "machineid"
        if machine_id_file.exists() or True:  # 总是创建
            new_machine_id = str(uuid.uuid4())
            with open(machine_id_file, 'w') as f:
                f.write(new_machine_id)
            self.log("   主机器ID已重置")
        
        # 增强：创建多个可能的机器ID文件
        additional_id_files = [
            "deviceid", "hardware_uuid", "system_uuid", 
            "platform_id", "installation_id"
        ]
        for id_file in additional_id_files:
            file_path = qoder_support_dir / id_file
            new_id = str(uuid.uuid4())
            with open(file_path, 'w') as f:
                f.write(new_id)
            self.log(f"   已创建: {id_file}")

        # 2. 重置遥测数据
        self.log("2. 重置遥测数据...")
        storage_json_file = qoder_support_dir / "User/globalStorage/storage.json"
        if storage_json_file.exists():
            with open(storage_json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            new_uuid = str(uuid.uuid4())
            machine_id_hash = hashlib.sha256(new_uuid.encode()).hexdigest()
            device_id = str(uuid.uuid4())
            sqm_id = str(uuid.uuid4())  # 新增：软件质量度量ID

            # 重置所有遥测相关的标识符（增强版）
            data['telemetry.machineId'] = machine_id_hash
            data['telemetry.devDeviceId'] = device_id
            data['telemetry.sqmId'] = sqm_id
            
            # 新增：重置更多可能的硬件指纹标识符
            data['telemetry.sessionId'] = str(uuid.uuid4())
            data['telemetry.installationId'] = str(uuid.uuid4())
            data['telemetry.clientId'] = str(uuid.uuid4())
            data['telemetry.userId'] = str(uuid.uuid4())
            data['telemetry.anonymousId'] = str(uuid.uuid4())
            data['machineId'] = machine_id_hash  # 备用机器ID
            data['deviceId'] = device_id  # 备用设备ID
            data['installationId'] = str(uuid.uuid4())  # 安装ID
            data['hardwareId'] = str(uuid.uuid4())  # 硬件ID
            data['platformId'] = str(uuid.uuid4())  # 平台ID
            
            # 重置系统指纹相关配置
            data['system.platform'] = 'darwin'  # 保持平台一致但重置其他
            data['system.arch'] = platform.machine()  # 重置架构信息
            data['system.version'] = f"{random.randint(10, 15)}.{random.randint(0, 9)}.{random.randint(0, 9)}"
            
            self.log(f"   新会话ID: {data['telemetry.sessionId'][:16]}...")
            self.log(f"   新安装ID: {data['telemetry.installationId'][:16]}...")
            self.log(f"   新硬件ID: {data['hardwareId'][:16]}...")
            
            # 清除其他可能的身份识别配置（保留对话时不清除）
            if not preserve_chat:
                # 完全重置模式：清除所有可能的身份相关配置
                identity_keys_to_remove = []
                for key in data.keys():
                    if any(keyword in key.lower() for keyword in [
                        'auth', 'login', 'session', 'token', 'credential',
                        'device', 'fingerprint', 'tracking', 'analytics'
                    ]):
                        identity_keys_to_remove.append(key)
                
                for key in identity_keys_to_remove:
                    del data[key]
                    self.log(f"   已清除配置: {key}")
            else:
                # 保留对话模式：只清除明确的身份识别配置
                self.log("   保留对话模式：保留非身份相关配置")

            with open(storage_json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            self.log(f"   新遥测机器ID: {machine_id_hash[:16]}...")
            self.log(f"   新设备ID: {device_id}")
            self.log(f"   新SQM ID: {sqm_id}")

        # 3. 清理缓存（增强版）
        self.log("3. 清理缓存数据...")
        cache_dirs = [
            "Cache", "blob_storage", "Code Cache", "SharedClientCache",
            "GPUCache", "DawnGraphiteCache", "DawnWebGPUCache",
            # 新增：更多可能包含指纹的缓存
            "ShaderCache", "DawnCache", "Dictionaries",
            "CachedData", "CachedProfilesData", "CachedExtensions",
            "IndexedDB", "CacheStorage", "WebSQL"
        ]

        cleaned = 0
        for cache_dir in cache_dirs:
            cache_path = qoder_support_dir / cache_dir
            if cache_path.exists():
                try:
                    shutil.rmtree(cache_path)
                    cleaned += 1
                except:
                    pass

        self.log(f"   已清理 {cleaned} 个缓存目录")
        
        # 4. 清理身份识别文件（增强版）
        self.log("4. 清理身份识别文件...")
        identity_files = [
            "Network Persistent State",  # 网络服务器连接历史和指纹
            "TransportSecurity",  # HSTS等安全策略记录
            "Trust Tokens", "Trust Tokens-journal",  # 信任令牌数据库
            "SharedStorage", "SharedStorage-wal",  # 共享存储数据库
            "Preferences",  # 用户偏好设置（可能包含指纹）
            "Secure Preferences",  # 安全偏好设置
            "Login Credentials",  # 登录凭据（如果存在）
            "Web Data", "Web Data-journal",  # Web数据数据库（如果存在）
            "cert_transparency_reporter_state.json",  # 证书透明度状态
            "Local State",  # Chromium本地状态（包含加密密钥）
            "NetworkDataMigrated",  # 网络数据迁移标记
            # 新增：硬件指纹相关文件
            "DeviceMetadata", "HardwareInfo", "SystemInfo",
            "QuotaManager", "QuotaManager-journal",
            "origin_bound_certs", "Network Action Predictor",
            "AutofillStrikeDatabase", "AutofillStrikeDatabase-journal",
            "Feature Engagement Tracker", "PasswordStoreDefault",
            "PreferredApps", "UserPrefs", "UserPrefs.backup",
            "Platform Notifications", "VideoDecodeStats",
            "OriginTrials", "BrowserMetrics", "SafeBrowsing",
            "Visited Links", "History", "History-journal",
            "Favicons", "Favicons-journal", "Shortcuts", "Shortcuts-journal",
            "Top Sites", "Top Sites-journal"
        ]
        
        identity_cleaned = 0
        for identity_file in identity_files:
            file_path = qoder_support_dir / identity_file
            if file_path.exists():
                try:
                    file_path.unlink()
                    self.log(f"   已清除: {identity_file}")
                    identity_cleaned += 1
                except Exception as e:
                    self.log(f"   清除失败 {identity_file}: {e}")
        
        # 5. 清理存储目录
        storage_dirs = [
            "Service Worker",  # 服务工作者缓存
            "Certificate Revocation Lists",  # 证书撤销列表
            "SSLCertificates",  # SSL证书缓存
            "databases",  # 数据库目录
            "clp",  # 剪贴板数据，可能包含敏感信息
            "logs",  # 日志文件，可能记录用户活动
            "Backups",  # 备份文件，可能包含历史身份信息
            "CachedExtensionVSIXs"  # 扩展缓存，显示用户安装的扩展
        ]
        
        # 根据是否保留对话记录来决定清理哪些存储目录
        if not preserve_chat:
            # 如果不保留对话记录，清理所有存储目录
            storage_dirs.extend([
                "Local Storage",  # 本地存储数据库（可能包含对话索引）
                "Session Storage",  # 会话存储
                "WebStorage",  # Web存储
                "Shared Dictionary"  # 共享字典
            ])
            self.log("   不保留对话模式：清理所有存储目录")
        else:
            # 如果保留对话记录，保留可能包含对话索引的存储
            # 但仍需清理可能包含身份信息的存储
            storage_dirs.extend([
                "Session Storage",  # 会话存储（可能包含身份信息）
                "WebStorage",  # Web存储（可能包含身份信息）
                "Shared Dictionary"  # 共享字典
            ])
            self.log("   保留对话模式：保留 Local Storage（可能包含对话索引）")
        
        for storage_dir in storage_dirs:
            storage_path = qoder_support_dir / storage_dir
            if storage_path.exists():
                try:
                    shutil.rmtree(storage_path)
                    self.log(f"   已清除: {storage_dir}")
                    identity_cleaned += 1
                except Exception as e:
                    self.log(f"   清除失败 {storage_dir}: {e}")
        
        self.log(f"   已清理 {identity_cleaned} 个身份识别文件/目录")
        
        # 5. 执行高级身份清理（新增）
        self.log("5. 执行高级身份清理...")
        self.perform_advanced_identity_cleanup(qoder_support_dir, preserve_chat)

        # 6. 执行登录身份清理（新增 - 清理登录状态）
        self.log("6. 执行登录身份清理...")
        self.perform_login_identity_cleanup(qoder_support_dir)

        # 7. 执行硬件指纹重置（新增 - 最强反检测）
        self.log("7. 执行硬件指纹重置...")
        self.perform_hardware_fingerprint_reset(qoder_support_dir)
        
        # 8. 执行超级深度清理（新增增强功能）
        self.log("8. 执行超级深度清理...")
        self.perform_super_deep_cleanup(qoder_support_dir)

        # 9. 处理对话记录
        if preserve_chat:
            self.log("9. 保留对话记录...")
            self.log("   对话记录已保留")
        else:
            self.log("9. 清除对话记录...")
            self.clear_chat_history(qoder_support_dir)

    def perform_advanced_identity_cleanup(self, qoder_support_dir, preserve_chat=False):
        """执行高级身份清理，清除所有可能的身份识别信息"""
        try:
            self.log("开始高级身份清理...")
            cleaned_count = 0
            
            # 1. 清理 SharedClientCache 内部文件
            shared_cache = qoder_support_dir / "SharedClientCache"
            if shared_cache.exists():
                # 总是清理这些关键的身份文件（会重新生成）
                critical_files = [".info", ".lock", "mcp.json"]
                for file_name in critical_files:
                    file_path = shared_cache / file_name
                    if file_path.exists():
                        try:
                            file_path.unlink()
                            self.log(f"   已清除: SharedClientCache/{file_name}")
                            cleaned_count += 1
                        except Exception as e:
                            self.log(f"   清除失败 {file_name}: {e}")
                
                # 总是清理 cache 目录（缓存数据）
                cache_dir = shared_cache / "cache"
                if cache_dir.exists():
                    try:
                        shutil.rmtree(cache_dir)
                        self.log("   已清除: SharedClientCache/cache")
                        cleaned_count += 1
                    except Exception as e:
                        self.log(f"   清除失败 cache: {e}")
                
                # 根据保留对话设置决定是否清理 index 目录
                index_dir = shared_cache / "index"
                if index_dir.exists():
                    if not preserve_chat:
                        # 不保留对话：清理所有索引
                        try:
                            shutil.rmtree(index_dir)
                            self.log("   已清除: SharedClientCache/index")
                            cleaned_count += 1
                        except Exception as e:
                            self.log(f"   清除失败 index: {e}")
                    else:
                        # 保留对话：只清理非对话相关的索引
                        # 保留可能包含对话搜索索引的文件
                        for index_item in index_dir.iterdir():
                            if index_item.is_dir() and 'chat' not in index_item.name.lower():
                                try:
                                    shutil.rmtree(index_item)
                                    self.log(f"   已清除: SharedClientCache/index/{index_item.name}")
                                    cleaned_count += 1
                                except Exception as e:
                                    self.log(f"   清除失败 index/{index_item.name}: {e}")
                        self.log("   保留对话模式：保留可能的对话索引")
            
            # 2. 清理系统级别的身份文件
            system_files = [
                "code.lock",
                "languagepacks.json"
            ]
            
            for sys_file in system_files:
                file_path = qoder_support_dir / sys_file
                if file_path.exists():
                    try:
                        file_path.unlink()
                        self.log(f"   已清除: {sys_file}")
                        cleaned_count += 1
                    except Exception as e:
                        self.log(f"   清除失败 {sys_file}: {e}")
            
            # 3. 清理崩溃报告目录（可能包含设备信息）
            crashpad_dir = qoder_support_dir / "Crashpad"
            if crashpad_dir.exists():
                try:
                    shutil.rmtree(crashpad_dir)
                    self.log("   已清除: Crashpad")
                    cleaned_count += 1
                except Exception as e:
                    self.log(f"   清除失败 Crashpad: {e}")
            
            # 4. 清理缓存目录（CachedData和 CachedProfilesData）
            cached_dirs = ["CachedData", "CachedProfilesData"]
            for cached_dir in cached_dirs:
                dir_path = qoder_support_dir / cached_dir
                if dir_path.exists():
                    try:
                        shutil.rmtree(dir_path)
                        self.log(f"   已清除: {cached_dir}")
                        cleaned_count += 1
                    except Exception as e:
                        self.log(f"   清除失败 {cached_dir}: {e}")
            
            # 5. 清理 socket 文件
            import glob
            socket_pattern = str(qoder_support_dir / "*.sock")
            socket_files = glob.glob(socket_pattern)
            for socket_file in socket_files:
                try:
                    Path(socket_file).unlink()
                    self.log(f"   已清除: {Path(socket_file).name}")
                    cleaned_count += 1
                except Exception as e:
                    self.log(f"   清除失败 {Path(socket_file).name}: {e}")
            
            # 6. 清理设备指纹和活动记录文件（新增）
            fingerprint_and_activity_files = [
                "DeviceMetadata", "HardwareInfo", "SystemInfo",
                "QuotaManager", "QuotaManager-journal",
                "ActivityLog", "EventLog", "UserActivityLog",
                "origin_bound_certs", "Network Action Predictor",
                "AutofillStrikeDatabase", "AutofillStrikeDatabase-journal",
                "Feature Engagement Tracker", "PasswordStoreDefault",
                "PreferredApps", "UserPrefs", "UserPrefs.backup"
            ]
            
            for file_name in fingerprint_and_activity_files:
                file_path = qoder_support_dir / file_name
                if file_path.exists():
                    try:
                        if file_path.is_dir():
                            shutil.rmtree(file_path)
                        else:
                            file_path.unlink()
                        self.log(f"   已清除: {file_name}")
                        cleaned_count += 1
                    except Exception as e:
                        self.log(f"   清除失败 {file_name}: {e}")
            
            # 7. 清理数据库目录内的所有文件（新增）
            databases_dir = qoder_support_dir / "databases"
            if databases_dir.exists():
                try:
                    shutil.rmtree(databases_dir)
                    self.log("   已清除: databases 目录及其所有内容")
                    cleaned_count += 1
                except Exception as e:
                    self.log(f"   清除失败 databases: {e}")
            
            # 8. 清理 Electron 相关的持久化数据（新增）
            electron_files = [
                "Dictionaries", "Platform Notifications",
                "ShaderCache", "VideoDecodeStats",
                "OriginTrials", "BrowserMetrics",
                "AutofillRegexes", "SafeBrowsing"
            ]
            
            for electron_file in electron_files:
                file_path = qoder_support_dir / electron_file
                if file_path.exists():
                    try:
                        if file_path.is_dir():
                            shutil.rmtree(file_path)
                        else:
                            file_path.unlink()
                        self.log(f"   已清除: {electron_file}")
                        cleaned_count += 1
                    except Exception as e:
                        self.log(f"   清除失败 {electron_file}: {e}")
            
            self.log(f"   高级身份清理完成，处理了 {cleaned_count} 个项目")
            
        except Exception as e:
            self.log(f"   高级身份清理失败: {e}")

    def clear_chat_history(self, qoder_support_dir):
        """清除对话记录"""
        try:
            cleared = 0

            # 1. 清除工作区中的对话会话
            workspace_storage = qoder_support_dir / "User/workspaceStorage"
            if workspace_storage.exists():
                for workspace_dir in workspace_storage.iterdir():
                    if workspace_dir.is_dir():
                        # 清除chatSessions目录
                        chat_sessions = workspace_dir / "chatSessions"
                        if chat_sessions.exists():
                            try:
                                shutil.rmtree(chat_sessions)
                                self.log(f"   已清除: {chat_sessions.relative_to(qoder_support_dir)}")
                                cleared += 1
                            except Exception as e:
                                self.log(f"   清除失败 {chat_sessions.relative_to(qoder_support_dir)}: {e}")

                        # 清除chatEditingSessions目录
                        chat_editing = workspace_dir / "chatEditingSessions"
                        if chat_editing.exists():
                            try:
                                shutil.rmtree(chat_editing)
                                self.log(f"   已清除: {chat_editing.relative_to(qoder_support_dir)}")
                                cleared += 1
                            except Exception as e:
                                self.log(f"   清除失败 {chat_editing.relative_to(qoder_support_dir)}: {e}")

            # 2. 清除历史记录
            history_dir = qoder_support_dir / "User/History"
            if history_dir.exists():
                try:
                    shutil.rmtree(history_dir)
                    self.log(f"   已清除: User/History")
                    cleared += 1
                except Exception as e:
                    self.log(f"   清除失败 User/History: {e}")

            # 3. 清除会话存储中的对话相关数据
            session_storage = qoder_support_dir / "Session Storage"
            if session_storage.exists():
                try:
                    shutil.rmtree(session_storage)
                    self.log(f"   已清除: Session Storage")
                    cleared += 1
                except Exception as e:
                    self.log(f"   清除失败 Session Storage: {e}")

            # 4. 清除用户数据中的对话相关配置
            user_data_file = qoder_support_dir / "User/globalStorage/storage.json"
            if user_data_file.exists():
                try:
                    with open(user_data_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    # 清除对话相关的键
                    chat_keys = [key for key in data.keys() if
                               'chat' in key.lower() or
                               'conversation' in key.lower() or
                               'history' in key.lower() or
                               'session' in key.lower()]

                    if chat_keys:
                        for key in chat_keys:
                            del data[key]
                            self.log(f"   已清除配置: {key}")

                        with open(user_data_file, 'w', encoding='utf-8') as f:
                            json.dump(data, f, indent=4, ensure_ascii=False)

                        cleared += 1

                except Exception as e:
                    self.log(f"   清除用户配置失败: {e}")

            self.log(f"   对话记录清除完成 (处理了 {cleared} 个项目)")

        except Exception as e:
            self.log(f"   清除对话记录失败: {e}")

    def open_github(self):
        """打开GitHub链接"""
        self.log("打开GitHub链接...")
        webbrowser.open("https://github.com/itandelin/qoder-free")
    
    def hardware_fingerprint_reset(self):
        """硬件指纹重置功能（增强防检测）"""
        self.log("开始硬件指纹重置...")

        # 检查Qoder是否在运行
        is_running, pids = self.check_qoder_running()
        if is_running:
            pid_info = self.tr('pid_info_single').format(pids[0]) if len(pids) == 1 else self.tr('pid_info_multiple').format(len(pids))
            reply = QMessageBox.question(self, self.tr('qoder_detected_running'),
                                       f"{self.tr('qoder_detected_running')}\n{pid_info}\n\n{self.tr('please_close_before_continue')}",
                                       QMessageBox.Yes | QMessageBox.No)
            if reply != QMessageBox.Yes:
                self.log("用户取消操作")
                return

            # 再次检查
            is_running, _ = self.check_qoder_running()
            if is_running:
                self.log("Qoder 仍在运行，操作取消")
                QMessageBox.critical(self, "错误", "请先完全关闭 Qoder 应用程序")
                return

        # 确认操作
        reply = QMessageBox.question(self, "确认硬件指纹重置",
                                   f"🔥 硬件指纹重置将：\n\n"
                                   f"• 重置所有硬件相关标识符\n"
                                   f"• 清除GPU、CPU、内存指纹\n"
                                   f"• 清除系统信息和平台标识\n"
                                   f"• 重置所有遥测和设备ID\n"
                                   f"• 清除所有硬件相关缓存\n"
                                   f"• 生成虚假硬件信息干扰检测\n\n"
                                   f"📝 这是最强的硬件指纹重置，确定继续吗？",
                                   QMessageBox.Yes | QMessageBox.No)
        if reply != QMessageBox.Yes:
            self.log("用户取消硬件指纹重置")
            return

        try:
            qoder_support_dir = self.get_qoder_data_dir()
            
            if not qoder_support_dir.exists():
                raise Exception("未找到 Qoder 应用数据目录")
            
            self.log("=" * 40)
            self.log("开始硬件指纹重置")
            self.log("=" * 40)
            
            # 执行硬件指纹重置
            self.perform_hardware_fingerprint_reset(qoder_support_dir)
            
            self.log("=" * 40)
            self.log(self.tr('hardware_fingerprint_completed') + "！")
            self.log("=" * 40)
            
            QMessageBox.information(self, self.tr('operation_complete'), self.tr('hardware_fingerprint_completed') + "！\n" + self.tr('suggest_restart_system') + "。")
            
        except Exception as e:
            self.log(f"硬件指纹重置失败: {e}")
            QMessageBox.critical(self, "错误", f"硬件指纹重置失败: {e}")
    
    def perform_hardware_fingerprint_reset(self, qoder_support_dir):
        """执行硬件指纹重置的具体实现"""
        try:
            self.log("开始硬件指纹重置...")
            reset_count = 0
            
            # 1. 重置所有可能的机器标识符
            self.log("1. 重置所有机器标识符...")
            machine_id_files = [
                "machineid", "deviceid", "hardware_uuid", "system_uuid",
                "platform_id", "installation_id", "cpu_id", "gpu_id",
                "board_serial", "bios_uuid", "memory_id"
            ]
            
            for id_file in machine_id_files:
                file_path = qoder_support_dir / id_file
                new_id = str(uuid.uuid4())
                try:
                    with open(file_path, 'w') as f:
                        f.write(new_id)
                    self.log(f"   ✅ 已重置: {id_file}")
                    reset_count += 1
                except Exception as e:
                    self.log(f"   ⚠️  重置失败 {id_file}: {e}")
            
            # 2. 重置 storage.json 中的所有硬件相关标识符
            self.log("2. 重置 storage.json 中的硬件标识符...")
            storage_file = qoder_support_dir / "User/globalStorage/storage.json"
            if storage_file.exists():
                try:
                    with open(storage_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # 生成全新的硬件标识符
                    hardware_identifiers = {
                        # 核心硬件标识符
                        'telemetry.machineId': hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest(),
                        'telemetry.devDeviceId': str(uuid.uuid4()),
                        'telemetry.sqmId': str(uuid.uuid4()),
                        'telemetry.sessionId': str(uuid.uuid4()),
                        'telemetry.installationId': str(uuid.uuid4()),
                        'telemetry.clientId': str(uuid.uuid4()),
                        'telemetry.userId': str(uuid.uuid4()),
                        'telemetry.anonymousId': str(uuid.uuid4()),
                        
                        # 备用标识符
                        'machineId': hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest(),
                        'deviceId': str(uuid.uuid4()),
                        'installationId': str(uuid.uuid4()),
                        'hardwareId': str(uuid.uuid4()),
                        'platformId': str(uuid.uuid4()),
                        'cpuId': str(uuid.uuid4()),
                        'gpuId': str(uuid.uuid4()),
                        'memoryId': str(uuid.uuid4()),
                        
                        # 系统指纹
                        'system.platform': 'darwin',
                        'system.arch': platform.machine(),
                        'system.version': f"{random.randint(10, 15)}.{random.randint(0, 9)}.{random.randint(0, 9)}",
                        'system.build': f"{random.randint(20000, 25000)}",
                        'system.locale': 'en-US',
                        'system.timezone': 'America/New_York'  # 随机时区
                    }
                    
                    # 更新所有标识符
                    for key, value in hardware_identifiers.items():
                        data[key] = value
                        self.log(f"   ✅ 已重置: {key}")
                    
                    # 清除其他可能的硬件指纹配置
                    hardware_keys_to_remove = []
                    for key in data.keys():
                        if any(keyword in key.lower() for keyword in [
                            'hardware', 'cpu', 'gpu', 'memory', 'disk', 'serial',
                            'mac', 'network', 'screen', 'resolution', 'vendor',
                            'model', 'brand', 'manufacturer', 'processor'
                        ]):
                            if key not in hardware_identifiers:  # 不删除已更新的键
                                hardware_keys_to_remove.append(key)
                    
                    for key in hardware_keys_to_remove:
                        del data[key]
                        self.log(f"   ✅ 已清除硬件指纹: {key}")
                    
                    with open(storage_file, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=4, ensure_ascii=False)
                    
                    reset_count += len(hardware_identifiers) + len(hardware_keys_to_remove)
                    self.log(f"   ✅ storage.json 硬件标识符重置完成")
                    
                except Exception as e:
                    self.log(f"   ⚠️  storage.json 处理失败: {e}")
            
            # 3. 清理硬件指纹相关文件
            self.log("3. 清理硬件指纹相关文件...")
            hardware_files = [
                "DeviceMetadata", "HardwareInfo", "SystemInfo",
                "GPUCache", "GPUInfo", "DawnGraphiteCache", "DawnWebGPUCache",
                "ShaderCache", "VideoDecodeStats", "MediaCache",
                "Platform Notifications", "Dictionaries",
                "QuotaManager", "QuotaManager-journal",
                "OriginTrials", "BrowserMetrics",
                # 新增：更多硬件检测文件
                "hardware_detection.json", "device_capabilities.json",
                "system_features.json", "platform_detection.dat",
                "cpu_features.json", "gpu_features.json",
                "memory_info.json", "display_info.json"
            ]
            
            for hardware_file in hardware_files:
                file_path = qoder_support_dir / hardware_file
                if file_path.exists():
                    try:
                        if file_path.is_dir():
                            shutil.rmtree(file_path)
                        else:
                            file_path.unlink()
                        self.log(f"   ✅ 已清除: {hardware_file}")
                        reset_count += 1
                    except Exception as e:
                        self.log(f"   ⚠️  清除失败 {hardware_file}: {e}")
            
            # 4. 清理硬件相关缓存
            self.log("4. 清理硬件相关缓存...")
            hardware_cache_dirs = [
                "GPUCache", "DawnGraphiteCache", "DawnWebGPUCache",
                "ShaderCache", "DawnCache", "MediaCache",
                "CachedData", "CachedProfilesData"
            ]
            
            for cache_dir in hardware_cache_dirs:
                dir_path = qoder_support_dir / cache_dir
                if dir_path.exists():
                    try:
                        shutil.rmtree(dir_path)
                        self.log(f"   ✅ 已清理缓存: {cache_dir}")
                        reset_count += 1
                    except Exception as e:
                        self.log(f"   ⚠️  清理失败 {cache_dir}: {e}")
            
            # 5. 创建虚假硬件信息文件（干扰检测）
            self.log("5. 创建虚假硬件信息...")
            try:
                # 根据系统类型生成相应的虚假硬件信息
                system_type = platform.system()
                self.log(f"   检测到系统类型: {system_type}")
                
                if system_type == "Darwin":  # macOS
                    fake_hardware_info = {
                        "cpu": {
                            "name": f"Apple M{random.randint(2, 5)} Pro",
                            "cores": random.choice([8, 10, 12, 16]),
                            "threads": random.choice([8, 10, 12, 16]),
                            "frequency": f"{random.uniform(2.0, 4.0):.1f}GHz"
                        },
                        "gpu": {
                            "name": f"Apple M{random.randint(2, 5)} Pro GPU",
                            "memory": f"{random.choice([16, 24, 32])}GB",
                            "cores": random.choice([16, 19, 24, 32])
                        },
                        "memory": {
                            "total": f"{random.choice([16, 24, 32, 64])}GB",
                            "type": "LPDDR5",
                            "speed": f"{random.choice([6400, 7467])}MT/s"
                        }
                    }
                elif system_type == "Windows":  # Windows
                    cpu_brands = ["Intel", "AMD"]
                    cpu_brand = random.choice(cpu_brands)
                    
                    if cpu_brand == "Intel":
                        cpu_series = random.choice(["Core i5", "Core i7", "Core i9"])
                        cpu_gen = random.randint(12, 14)
                        cpu_model = f"{random.randint(600, 900)}{'K' if random.choice([True, False]) else ''}"
                        cpu_name = f"Intel {cpu_series}-{cpu_gen}{cpu_model}"
                    else:  # AMD
                        cpu_series = random.choice(["Ryzen 5", "Ryzen 7", "Ryzen 9"])
                        cpu_gen = random.randint(5000, 7000)
                        cpu_name = f"AMD {cpu_series} {cpu_gen}X"
                    
                    gpu_brands = ["NVIDIA", "AMD", "Intel"]
                    gpu_brand = random.choice(gpu_brands)
                    
                    if gpu_brand == "NVIDIA":
                        gpu_series = random.choice(["RTX 4060", "RTX 4070", "RTX 4080", "RTX 4090"])
                        gpu_name = f"NVIDIA GeForce {gpu_series}"
                        gpu_memory = f"{random.choice([8, 12, 16, 24])}GB"
                    elif gpu_brand == "AMD":
                        gpu_series = random.choice(["RX 7600", "RX 7700 XT", "RX 7800 XT", "RX 7900 XTX"])
                        gpu_name = f"AMD Radeon {gpu_series}"
                        gpu_memory = f"{random.choice([8, 12, 16, 20])}GB"
                    else:  # Intel
                        gpu_series = random.choice(["Arc A750", "Arc A770", "Iris Xe"])
                        gpu_name = f"Intel {gpu_series}"
                        gpu_memory = f"{random.choice([8, 12, 16])}GB"
                    
                    fake_hardware_info = {
                        "cpu": {
                            "name": cpu_name,
                            "cores": random.choice([6, 8, 12, 16, 24]),
                            "threads": random.choice([12, 16, 20, 24, 32]),
                            "frequency": f"{random.uniform(3.0, 5.0):.1f}GHz"
                        },
                        "gpu": {
                            "name": gpu_name,
                            "memory": gpu_memory,
                            "cores": random.choice([1024, 1536, 2048, 2560])
                        },
                        "memory": {
                            "total": f"{random.choice([16, 24, 32])}GB",
                            "type": "LPDDR5",
                            "speed": f"{random.choice([4266, 5500, 6400])}MHz"
                        }
                    }
                elif system_type == "Windows":  # Windows
                    cpu_brands = ["Intel", "AMD"]
                    cpu_brand = random.choice(cpu_brands)
                    
                    if cpu_brand == "Intel":
                        # Intel 处理器
                        generations = ["12th", "13th", "14th"]
                        gen = random.choice(generations)
                        cpu_num = random.randint(12400, 14900)
                        cpu_name = f"Intel Core i{random.choice([5, 7, 9])}-{cpu_num}"
                    else:
                        # AMD 处理器
                        series = random.choice(["5000", "7000", "9000"])
                        cpu_num = random.randint(5600, 9950)
                        cpu_name = f"AMD Ryzen {random.choice([5, 7, 9])} {cpu_num}X"
                    
                    # Windows 显卡选择
                    gpu_options = [
                        "NVIDIA GeForce RTX 4060",
                        "NVIDIA GeForce RTX 4070", 
                        "NVIDIA GeForce RTX 4080",
                        "AMD Radeon RX 7600",
                        "AMD Radeon RX 7700 XT",
                        "AMD Radeon RX 7800 XT",
                        "Intel Arc A770",
                        "Intel UHD Graphics 770"
                    ]
                    
                    fake_hardware_info = {
                        "cpu": {
                            "name": cpu_name,
                            "cores": random.choice([6, 8, 12, 16, 20]),
                            "threads": random.choice([12, 16, 20, 24, 32]),
                            "frequency": f"{random.uniform(3.0, 5.5):.1f}GHz"
                        },
                        "gpu": {
                            "name": random.choice(gpu_options),
                            "memory": f"{random.choice([8, 12, 16, 24])}GB",
                            "driver_version": f"{random.randint(530, 560)}.{random.randint(60, 99)}"
                        },
                        "memory": {
                            "total": f"{random.choice([16, 32, 64, 128])}GB",
                            "type": random.choice(["DDR4", "DDR5"]),
                            "speed": f"{random.choice([3200, 3600, 4800, 5600])}MHz"
                        }
                    }
                else:  # Linux 或其他系统
                    cpu_brands = ["Intel", "AMD"]
                    cpu_brand = random.choice(cpu_brands)
                    
                    if cpu_brand == "Intel":
                        cpu_name = f"Intel Core i{random.choice([5, 7, 9])}-{random.randint(10400, 13900)}K"
                    else:
                        cpu_name = f"AMD Ryzen {random.choice([5, 7, 9])} {random.randint(5600, 7900)}X"
                    
                    fake_hardware_info = {
                        "cpu": {
                            "name": cpu_name,
                            "cores": random.choice([4, 6, 8, 12, 16]),
                            "threads": random.choice([8, 12, 16, 24, 32]),
                            "frequency": f"{random.uniform(2.5, 4.8):.1f}GHz"
                        },
                        "gpu": {
                            "name": random.choice(["NVIDIA GeForce RTX 4060", "AMD Radeon RX 7600", "Intel Arc A750"]),
                            "memory": f"{random.choice([4, 8, 12, 16])}GB",
                            "cores": random.choice([896, 1024, 1408, 1792])
                        },
                        "memory": {
                            "total": f"{random.choice([8, 16, 32])}GB",
                            "type": random.choice(["DDR4", "DDR5"]),
                            "speed": f"{random.choice([2666, 3200, 3600])}MHz"
                        }
                    }
                
                # 添加通用的显示和系统信息
                if system_type == "Darwin":
                    display_resolutions = ["2560x1440", "3024x1964", "3456x2234", "5120x2880"]
                elif system_type == "Windows":
                    display_resolutions = ["1920x1080", "2560x1440", "3440x1440", "3840x2160"]
                else:
                    display_resolutions = ["1920x1080", "2560x1440", "1366x768", "3840x2160"]
                
                fake_hardware_info.update({
                    "display": {
                        "resolution": random.choice(display_resolutions),
                        "scale": random.choice([1.0, 1.25, 1.5, 2.0]),
                        "refresh_rate": random.choice([60, 75, 120, 144, 165])
                    },
                    "system": {
                        "platform": system_type.lower(),
                        "arch": platform.machine(),
                        "version": self.generate_system_version(system_type)
                    },
                    "fingerprint_reset": {
                        "timestamp": datetime.now().isoformat(),
                        "version": "2.2.1-enhanced",
                        "reset_id": str(uuid.uuid4()),
                        "system_detected": system_type
                    }
                })
                
                # 写入多个虚假文件
                fake_files = [
                    "hardware_detection.json",
                    "device_capabilities.json", 
                    "system_features.json"
                ]
                
                for fake_file in fake_files:
                    file_path = qoder_support_dir / fake_file
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(fake_hardware_info, f, indent=2, ensure_ascii=False)
                    
                    # 在 macOS 上设置为隐藏文件
                    try:
                        subprocess.run(['chflags', 'hidden', str(file_path)], check=False)
                    except:
                        pass
                    
                    self.log(f"   ✅ 已创建虚假信息: {fake_file}")
                    reset_count += 1
                
            except Exception as e:
                self.log(f"   ⚠️  创建虚假信息失败: {e}")
            
            # 6. 系统级缓存清理（新增增强功能）
            self.log("6. 清理系统级缓存...")
            self.clear_system_level_caches()
            
            # 7. 网络配置重置（新增增强功能）
            self.log("7. 重置网络相关配置...")
            self.reset_network_traces()
            
            # 8. 浏览器User-Agent混淆（新增增强功能）
            self.log("8. 混淆浏览器指纹...")
            self.obfuscate_browser_fingerprint(qoder_support_dir)
            
            self.log(f"   {self.tr('hardware_fingerprint_completed')}，处理了 {reset_count} 个项目")
            
        except Exception as e:
            self.log(f"   硬件指纹重置失败: {e}")
    
    def clear_system_level_caches(self):
        """🛡️ 安全清理系统级缓存（仅清理与Qoder相关的缓存，不影响其他应用）"""
        try:
            system_type = platform.system()
            
            if system_type == "Darwin":  # macOS
                # ✅ 安全模式：只清理与Qoder/VSCode/Electron相关的系统级缓存
                self.log("   🔍 安全模式：仅清理与Qoder相关的系统缓存...")
                
                # 🛡️ 白名单模式 - 只清理明确与这些应用相关的缓存
                safe_cache_patterns = [
                    "com.microsoft.VSCode",
                    "qoder", "Qoder", "QODER",
                    "vscode", "VSCode", "Visual Studio Code",
                    "Electron", "electron"
                ]
                
                # 📂 只在特定的缓存目录中查找
                base_cache_dirs = [
                    Path.home() / "Library/Caches",
                    Path.home() / "Library/HTTPStorages",
                    Path.home() / "Library/WebKit",
                    Path.home() / "Library/Application Support/CrashReporter"
                ]
                
                cleaned_count = 0
                for base_dir in base_cache_dirs:
                    if base_dir.exists():
                        try:
                            for item in base_dir.iterdir():
                                # 🔍 严格匹配：必须完全匹配模式才清理
                                should_clean = False
                                item_name_lower = item.name.lower()
                                
                                for pattern in safe_cache_patterns:
                                    if pattern.lower() in item_name_lower:
                                        # 📋 额外安全检查：避免误删重要系统文件
                                        dangerous_keywords = ['system', 'apple', 'safari', 'chrome', 'firefox', 'mail', 'finder']
                                        is_safe = not any(dangerous in item_name_lower for dangerous in dangerous_keywords)
                                        
                                        if is_safe:
                                            should_clean = True
                                            break
                                
                                if should_clean:
                                    try:
                                        if item.is_dir():
                                            shutil.rmtree(item)
                                        else:
                                            item.unlink()
                                        self.log(f"   ✅ 已安全清理: {item.name}")
                                        cleaned_count += 1
                                    except Exception as e:
                                        self.log(f"   ⚠️  清理失败 {item.name}: {e}")
                        except Exception as e:
                            self.log(f"   ⚠️  访问失败 {base_dir.name}: {e}")
                
                # 🚫 跳过可能影响系统的DNS缓存清理
                self.log("   🛡️ 安全保护：跳过DNS缓存清理以保护系统网络功能")
                
                if cleaned_count > 0:
                    self.log(f"   ✅ 安全清理完成：处理了 {cleaned_count} 个Qoder相关缓存项")
                else:
                    self.log("   ℹ️  未发现需要清理的Qoder相关缓存（这是正常的）")
                    
            elif system_type == "Windows":
                # 🖥️ Windows 安全模式：只清理用户级别的Qoder相关缓存
                self.log("   🔍 Windows安全模式：仅清理用户级Qoder相关缓存...")
                try:
                    # 📁 只清理当前用户的临时文件中与Qoder相关的内容
                    temp_dir = Path(os.environ.get('TEMP', ''))
                    app_data = Path(os.environ.get('LOCALAPPDATA', ''))
                    
                    safe_dirs = [temp_dir, app_data / "Temp"]
                    cleaned_count = 0
                    
                    for safe_dir in safe_dirs:
                        if safe_dir.exists():
                            for item in safe_dir.iterdir():
                                item_name_lower = item.name.lower()
                                if any(keyword in item_name_lower for keyword in ['qoder', 'vscode', 'code-', 'electron']):
                                    # 🛡️ 避免删除系统重要文件
                                    if not any(sys_keyword in item_name_lower for sys_keyword in ['system', 'microsoft', 'windows', 'temp']):
                                        try:
                                            if item.is_dir():
                                                shutil.rmtree(item)
                                            else:
                                                item.unlink()
                                            self.log(f"   ✅ 已清理Windows缓存: {item.name}")
                                            cleaned_count += 1
                                        except Exception as e:
                                            self.log(f"   ⚠️  清理失败 {item.name}: {e}")
                    
                    self.log(f"   🛡️ Windows安全清理完成：处理了 {cleaned_count} 个项目")
                    self.log("   ℹ️  跳过系统级操作以保护Windows系统稳定性")
                except Exception as e:
                    self.log(f"   ⚠️  Windows缓存清理失败: {e}")
            
            else:  # Linux
                self.log("   🐧 Linux安全模式：仅清理用户级Qoder相关缓存...")
                try:
                    # 📁 清理用户缓存目录中的相关文件
                    cache_dirs = [
                        Path.home() / ".cache",
                        Path.home() / ".config",
                        Path.home() / ".local/share"
                    ]
                    
                    cleaned_count = 0
                    for cache_dir in cache_dirs:
                        if cache_dir.exists():
                            for item in cache_dir.iterdir():
                                item_name_lower = item.name.lower()
                                if any(keyword in item_name_lower for keyword in ['qoder', 'vscode', 'code', 'electron']):
                                    # 🛡️ 避免删除系统配置文件
                                    if not any(sys_keyword in item_name_lower for sys_keyword in ['dbus', 'systemd', 'pulse', 'gtk']):
                                        try:
                                            if item.is_dir():
                                                shutil.rmtree(item)
                                            else:
                                                item.unlink()
                                            self.log(f"   ✅ 已清理Linux缓存: {item.name}")
                                            cleaned_count += 1
                                        except Exception as e:
                                            self.log(f"   ⚠️  清理失败 {item.name}: {e}")
                    
                    self.log(f"   🐧 Linux安全清理完成：处理了 {cleaned_count} 个项目")
                except Exception as e:
                    self.log(f"   ⚠️  Linux缓存清理失败: {e}")
                    
        except Exception as e:
            self.log(f"   ❌ 系统级缓存清理失败: {e}")
    
    def reset_network_traces(self):
        """重置网络痕迹（新增增强功能）"""
        try:
            qoder_support_dir = self.get_qoder_data_dir()
            
            # 清理更多网络相关文件
            network_files = [
                "Network Persistent State",
                "TransportSecurity", 
                "Trust Tokens",
                "Trust Tokens-journal",
                "Network Action Predictor",
                "NetworkDataMigrated",
                "Reporting and NEL",
                "HSTS",
                "Certificate Transparency Reporter State",
                "cert_transparency_reporter_state.json",
                "Certificate Revocation Lists",
                "SSLCertificates",
                "Cookies",
                "Cookies-journal",
                "QuotaManager",
                "QuotaManager-journal"
            ]
            
            cleared_count = 0
            for network_file in network_files:
                file_path = qoder_support_dir / network_file
                if file_path.exists():
                    try:
                        if file_path.is_dir():
                            shutil.rmtree(file_path)
                        else:
                            file_path.unlink()
                        self.log(f"   ✅ 已清除网络文件: {network_file}")
                        cleared_count += 1
                    except Exception as e:
                        self.log(f"   ⚠️  清除失败 {network_file}: {e}")
            
            # 重新生成网络配置文件（创建干净的网络状态）
            try:
                network_state_file = qoder_support_dir / "Network Persistent State"
                empty_network_state = {
                    "net": {
                        "http_server_properties": {},
                        "transport_security_persister": {},
                        "dns_config": {},
                        "ssl_config_service": {}
                    }
                }
                
                with open(network_state_file, 'w', encoding='utf-8') as f:
                    json.dump(empty_network_state, f, indent=2)
                
                self.log("   ✅ 已重新生成网络状态文件")
                cleared_count += 1
            except Exception as e:
                self.log(f"   ⚠️  重新生成网络状态失败: {e}")
            
            self.log(f"   网络痕迹清理完成，处理了 {cleared_count} 个文件")
            
        except Exception as e:
            self.log(f"   网络痕迹重置失败: {e}")
    
    def obfuscate_browser_fingerprint(self, qoder_support_dir):
        """混淆浏览器指纹（新增增强功能）"""
        try:
            # 创建混淆的浏览器配置
            user_agent_list = [
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ]
            
            fingerprint_data = {
                "user_agent": random.choice(user_agent_list),
                "screen_resolution": random.choice(["1920x1080", "2560x1440", "3840x2160", "1366x768"]),
                "color_depth": random.choice([24, 32]),
                "timezone": random.choice(["America/New_York", "Europe/London", "Asia/Tokyo", "America/Los_Angeles"]),
                "language": random.choice(["en-US", "en-GB", "zh-CN", "ja-JP"]),
                "platform": random.choice(["MacIntel", "Win32", "Linux x86_64"]),
                "webgl_vendor": random.choice(["Google Inc. (Apple)", "Google Inc. (NVIDIA)", "Google Inc. (Intel)"]),
                "canvas_fingerprint": hashlib.md5(str(random.random()).encode()).hexdigest()[:16],
                "audio_fingerprint": hashlib.md5(str(random.random()).encode()).hexdigest()[:16],
                "fonts": random.sample([
                    "Arial", "Helvetica", "Times", "Courier", "Verdana", "Georgia", 
                    "Palatino", "Garamond", "Bookman", "Comic Sans MS", "Trebuchet MS", "Impact"
                ], k=random.randint(5, 10)),
                "plugins": random.sample([
                    "Chrome PDF Plugin", "Chrome PDF Viewer", "Native Client", 
                    "Widevine Content Decryption Module", "Shockwave Flash"
                ], k=random.randint(2, 4))
            }
            
            # 保存浏览器指纹混淆数据
            fingerprint_files = [
                "browser_fingerprint.json",
                "canvas_fingerprint.json", 
                "webgl_fingerprint.json",
                "audio_fingerprint.json"
            ]
            
            for fp_file in fingerprint_files:
                file_path = qoder_support_dir / fp_file
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(fingerprint_data, f, indent=2, ensure_ascii=False)
                
                # 在 macOS 上设置为隐藏文件
                try:
                    subprocess.run(['chflags', 'hidden', str(file_path)], check=False)
                except:
                    pass
                
                self.log(f"   ✅ 已创建指纹混淆: {fp_file}")
            
            # 修改现有的 Preferences 文件以注入混淆数据
            prefs_file = qoder_support_dir / "Preferences"
            if prefs_file.exists():
                try:
                    with open(prefs_file, 'r', encoding='utf-8') as f:
                        prefs_data = json.load(f)
                    
                    # 注入混淆的浏览器信息
                    prefs_data.update({
                        "browser.user_agent_override": fingerprint_data["user_agent"],
                        "intl.accept_languages": fingerprint_data["language"],
                        "general.useragent.override": fingerprint_data["user_agent"],
                        "privacy.resistFingerprinting": True,
                        "privacy.fingerprintingProtection": True
                    })
                    
                    with open(prefs_file, 'w', encoding='utf-8') as f:
                        json.dump(prefs_data, f, indent=2, ensure_ascii=False)
                    
                    self.log("   ✅ 已混淆 Preferences 文件")
                except Exception as e:
                    self.log(f"   ⚠️  Preferences 混淆失败: {e}")
            
            self.log("   浏览器指纹混淆完成")
            
        except Exception as e:
            self.log(f"   浏览器指纹混淆失败: {e}")
    
    def perform_super_deep_cleanup(self, qoder_support_dir):
        """🛡️ 执行超级深度清理（安全增强版，只清理与Qoder相关的文件）"""
        try:
            self.log("🔥 开始安全的超级深度清理...")
            cleaned_count = 0
            
            # 1. 清理系统级别的身份文件
            self.log("1. 清理系统级别身份文件...")
            system_identity_files = [
                # 日志和临时文件
                "logs", "tmp", "temp", "crash_dumps",
                # 更多可能的身份识别文件
                "identity.json", "machine.json", "device.json",
                "fingerprint.json", "tracking.json", "analytics.json",
                # 浏览器相关文件
                "BrowserUserAgent", "ClientHints", "NavigatorInfo",
                "ScreenInfo", "TimezoneInfo", "LanguageInfo",
                # 网络相关文件
                "DNSCache", "HTTPCache", "ProxySettings",
                "NetworkConfiguration", "ConnectionHistory",
                # 系统信息文件
                "OSInfo", "HardwareProfile", "SystemMetrics",
                "PerformanceInfo", "MemoryInfo", "DiskInfo",
                # 用户活动相关
                "UserActivity", "AppUsage", "FeatureUsage",
                "InteractionHistory", "AccessLog", "AuditLog",
                # 安全相关文件
                "SecuritySettings", "CertificateStore", "TrustStore",
                "EncryptionKeys", "AuthTokens", "SessionKeys",
                # 缓存相关文件
                "MetadataCache", "ThumbnailCache", "IndexCache",
                "SearchCache", "QueryCache", "ResultsCache",
                # 扩展和插件相关
                "ExtensionData", "PluginData", "AddonData",
                "ExtensionPrefs", "PluginPrefs", "AddonPrefs",
                # 更多 WebKit 相关文件
                "WebKitCache", "WebProcessCache", "PluginProcessCache",
                "RenderProcessCache", "GPUProcessCache",
                # 更多 Chromium 相关文件
                "ChromiumState", "ChromiumPrefs", "ChromiumHistory",
                "ChromiumCookies", "ChromiumSessions"
            ]
            
            for file_name in system_identity_files:
                file_path = qoder_support_dir / file_name
                if file_path.exists():
                    try:
                        if file_path.is_dir():
                            shutil.rmtree(file_path)
                        else:
                            file_path.unlink()
                        self.log(f"   ✅ 已清除: {file_name}")
                        cleaned_count += 1
                    except Exception as e:
                        self.log(f"   ⚠️  清除失败 {file_name}: {e}")
            
            # 2. 谨慎清理指定扩展名的可疑文件（增加安全检查）
            self.log("2. 谨慎清理可疑扩展名文件...")
            suspicious_extensions = [
                ".tmp", ".temp", ".cache", ".lock", ".pid", ".sock", 
                ".session", ".fingerprint", ".tracking", ".analytics"
            ]
            
            # 🚫 绝对安全白名单 - 永远不删除的重要文件
            protected_keywords = [
                "settings", "config", "workspace", "preference", "user",
                "important", "backup", "license", "key", "certificate", 
                "password", "auth", "secret", "critical", "system",
                "apple", "microsoft", "windows", "macos", "safari", "chrome"
            ]
            
            # ✅ 只清理与这些应用相关的文件
            qoder_keywords = ['qoder', 'vscode', 'electron', 'code-', 'ms-vscode']
            
            for root, dirs, files in os.walk(qoder_support_dir):
                for file in files:
                    file_path = Path(root) / file
                    file_ext = file_path.suffix.lower()
                    
                    if file_ext in suspicious_extensions:
                        # 🛡️ 多重安全检查
                        is_protected = any(keyword in file.lower() for keyword in protected_keywords)
                        is_in_qoder_dir = str(qoder_support_dir) in str(file_path)
                        is_qoder_related = any(keyword in file.lower() or keyword in root.lower() 
                                             for keyword in qoder_keywords)
                        
                        # ✅ 只有同时满足以下条件才删除：
                        # 1. 在Qoder目录内  2. 与Qoder相关  3. 不在保护列表
                        if is_in_qoder_dir and is_qoder_related and not is_protected:
                            try:
                                file_path.unlink()
                                self.log(f"   ✅ 已清除可疑文件: {file}")
                                cleaned_count += 1
                            except Exception as e:
                                self.log(f"   ⚠️  清除失败 {file}: {e}")
                        else:
                            if not is_qoder_related:
                                self.log(f"   ℹ️  跳过非相关文件: {file}")
                            if is_protected:
                                self.log(f"   ℹ️  保护重要文件: {file}")
            
            # 3. 清理隐藏文件和目录
            self.log("3. 清理隐藏文件...")
            for root, dirs, files in os.walk(qoder_support_dir):
                # 清理隐藏文件（以点开头）
                for file in files:
                    if file.startswith('.') and file not in ['.gitignore', '.gitkeep']:
                        file_path = Path(root) / file
                        try:
                            file_path.unlink()
                            self.log(f"   ✅ 已清除隐藏文件: {file}")
                            cleaned_count += 1
                        except Exception as e:
                            self.log(f"   ⚠️  清除失败 {file}: {e}")
                
                # 清理隐藏目录（以点开头）
                for dir_name in dirs[:]:
                    if dir_name.startswith('.') and dir_name not in ['.git']:
                        dir_path = Path(root) / dir_name
                        try:
                            shutil.rmtree(dir_path)
                            self.log(f"   ✅ 已清除隐藏目录: {dir_name}")
                            dirs.remove(dir_name)  # 从遍历中移除
                            cleaned_count += 1
                        except Exception as e:
                            self.log(f"   ⚠️  清除失败 {dir_name}: {e}")
            
            # 4. 重置文件权限（防止文件时间戳检测）
            self.log("4. 重置文件权限...")
            try:
                # 重置整个目录的权限
                if platform.system() != "Windows":
                    subprocess.run(['chmod', '-R', '755', str(qoder_support_dir)], check=False, timeout=30)
                    self.log("   ✅ 文件权限已重置")
            except Exception as e:
                self.log(f"   ⚠️  权限重置失败: {e}")
            
            # 5. 创建迷惑性文件（干扰检测）
            self.log("5. 创建迷惑性文件...")
            try:
                decoy_files = [
                    "real_machine_id.tmp", "backup_device_id.log", 
                    "old_telemetry.dat", "previous_session.cache",
                    "legacy_fingerprint.json", "archived_identity.bak",
                    "system_backup.tmp", "device_clone.dat"
                ]
                
                for decoy_file in decoy_files:
                    file_path = qoder_support_dir / decoy_file
                    fake_data = {
                        "fake_id": str(uuid.uuid4()),
                        "timestamp": (datetime.now() - timedelta(days=random.randint(30, 365))).isoformat(),
                        "data": hashlib.md5(str(random.random()).encode()).hexdigest(),
                        "note": "This is a decoy file"
                    }
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(fake_data, f, indent=2)
                    
                    # 设置为隐藏文件
                    try:
                        if platform.system() == "Darwin":
                            subprocess.run(['chflags', 'hidden', str(file_path)], check=False)
                    except:
                        pass
                    
                    self.log(f"   ✅ 已创建迷惑文件: {decoy_file}")
                    cleaned_count += 1
            except Exception as e:
                self.log(f"   ⚠️  创建迷惑文件失败: {e}")
            
            # 6. 安全清理系统级别的缓存（macOS）
            if platform.system() == "Darwin":
                self.log("6. 安全清理 macOS 系统级缓存...")
                try:
                    # 只清理用户级别的系统缓存，不影响系统稳定性
                    user_system_cache_paths = [
                        Path.home() / "Library/Caches",
                        Path.home() / "Library/Application Support/com.apple.sharedfilelist",
                    ]
                    
                    for cache_path in user_system_cache_paths:
                        if cache_path.exists() and cache_path != qoder_support_dir:
                            # 只清理与 Qoder/VSCode 相关的文件，不影响其他应用
                            for item in cache_path.iterdir():
                                item_name_lower = item.name.lower()
                                if any(keyword in item_name_lower for keyword in 
                                      ['qoder', 'vscode', 'com.microsoft.vscode', 'electron']):
                                    try:
                                        if item.is_dir():
                                            shutil.rmtree(item)
                                        else:
                                            item.unlink()
                                        self.log(f"   ✅ 已清理系统缓存: {item.name}")
                                        cleaned_count += 1
                                    except Exception as e:
                                        self.log(f"   ⚠️  系统缓存清理失败 {item.name}: {e}")
                    
                    # 不清理 LaunchServices，避免影响系统功能
                    self.log("   ℹ️  为保护系统稳定性，跳过 LaunchServices 清理")
                    
                except Exception as e:
                    self.log(f"   ⚠️  macOS 系统缓存清理失败: {e}")
            
            elif platform.system() == "Windows":
                self.log("6. 安全清理 Windows 系统级缓存...")
                try:
                    # 只清理用户级别的缓存，不影响系统
                    user_cache_paths = [
                        Path(os.environ.get('LOCALAPPDATA', '')) / "Temp",
                        Path(os.environ.get('APPDATA', '')) / "Microsoft" / "Windows" / "Recent"
                    ]
                    
                    for cache_path in user_cache_paths:
                        if cache_path.exists():
                            for item in cache_path.iterdir():
                                if any(keyword in item.name.lower() for keyword in ['qoder', 'vscode', 'electron']):
                                    try:
                                        if item.is_dir():
                                            shutil.rmtree(item)
                                        else:
                                            item.unlink()
                                        self.log(f"   ✅ 已清理Windows缓存: {item.name}")
                                        cleaned_count += 1
                                    except Exception as e:
                                        self.log(f"   ⚠️  清理失败: {e}")
                except Exception as e:
                    self.log(f"   ⚠️  Windows 系统缓存清理失败: {e}")
            
            self.log(f"   超级深度清理完成，处理了 {cleaned_count} 个项目")
            
        except Exception as e:
            self.log(f"   超级深度清理失败: {e}")

def main():
    app = QApplication(sys.argv)

    # 设置应用程序样式
    app.setStyle('Fusion')

    # 设置全局样式表，确保对话框文字和按钮可见
    app.setStyleSheet("""
        QMessageBox {
            background-color: white;
            color: black;
        }
        QMessageBox QLabel {
            color: black;
        }
        QMessageBox QPushButton {
            background-color: white;
            color: black;
            border: 1px solid #ccc;
            padding: 5px 15px;
        }
    """)

    window = QoderResetGUI()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
