class StompFrame(object):

    @staticmethod
    def ok():
        #TODO no such command - use empty message with weird byte

        f = StompFrame()
        f.build_frame({"command": 'OK'})

        return f

    @staticmethod
    def connected():
        f = StompFrame()

        f.build_frame({
            "command": 'CONNECTED',
            "headers": {},
            "body": None
        })

        return f

    @staticmethod
    def message(message):
    #        assert command
        f = StompFrame()

        f.build_frame({
            "command": 'MESSAGE',
            "headers": {},
            "body": message
        })

        return f

    def parse_headers(self, headers_str):
        """Parse headers received from the servers and convert
        to a :class:`dict`.i

        :param headers_str: String to parse headers from

        """
        # george:constanza\nelaine:benes
        # -> {"george": "constanza", "elaine": "benes"}

        headers = {}
        message_raw = headers_str.split("\n")
        for line in message_raw[1:]:
            tokens = line.split(":")
            if len(tokens) == 2 and tokens[0]:
                headers[tokens[0].strip()] = tokens[1].strip()

        return headers

    def build_frame(self, args, want_receipt=False):
        """Build a frame based on a :class:`dict` of arguments.

        :param args: A :class:`dict` of arguments for the frame.

        :keyword want_receipt: Optional argument to get a receipt from
            the sever that the frame was received.

        Example

            >>> frame = frameobj.build_frame({"command": 'CONNECT',
                                              "headers": {},
                                              want_receipt=True)
        """
        self.command = args.get('command')
        self.headers = args.get('headers')
        self.body = args.get('body')
        if want_receipt:
            receipt_stamp = str(random.randint(0, 10000000))
            self.headers["receipt"] = "%s-%s" % (
                    self.session.get("session"), receipt_stamp)
        return self

    def as_string(self):
        """Raw string representation of this frame
        Suitable for passing over a socket to the STOMP server.

        Example

            >>> stomp.send(frameobj.as_string())

        """
        command = self.command
        headers = self.headers
        body = self.body

        bytes_message = False
        if 'bytes_message' in headers:
            bytes_message = True
            del headers['bytes_message']
            headers['content-length'] = len(body)
        headers['x-client'] = self.my_name

        # Convert and append any existing headers to a string as the
        # protocol describes.
        headerparts = ("%s:%s\n" % (key, value)
                            for key, value in headers.iteritems())

        # Frame is Command + Header + EOF marker.
        frame = "%s\n%s\n%s\x00" % (command, "".join(headerparts), body)

        return frame

    def parse_command(self, command_str):
        """Parse command received from the server.

        :param command_str: String to parse command from

        """
        command = command_str.split('\n', 1)[0]
        return command
