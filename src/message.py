class Message():
    def __init__(self, m_sender, m_text, m_type, m_timestamp, t_dst=None, t_src=None):
        self.m_sender = m_sender
        self.m_text = m_text
        self.m_type = m_type
        self.m_timestamp = m_timestamp
        self.t_dst = t_dst
        self.t_src = t_src
