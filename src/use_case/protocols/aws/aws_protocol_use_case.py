from src.use_case.protocols.aws.delete_aws_protocol_use_case import (
    AwsDeleteProtocolUseCase,
)
from src.use_case.protocols.aws.update_upload_aws_protocol_use_case import (
    AwsUpdateUploadProtocolUseCase,
)
from src.use_case.protocols.aws.upload_aws_protocol_use_case import (
    AwsUploadProtocolUseCase,
)


class AwsProtocolUseCase(
    AwsUploadProtocolUseCase, AwsDeleteProtocolUseCase, AwsUpdateUploadProtocolUseCase
):
    pass
