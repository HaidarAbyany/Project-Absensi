from marshmallow import Schema, fields, validate

class PembayaranSchema(Schema):
    id = fields.String(dump_only=True)
    tgl_bayar = fields.String(required=True)
    bulan_bayar = fields.String(required=True)
    tahun_bayar = fields.String(required=True)
    jumlah_bayar = fields.String(required=True)
    name = fields.String(required=True)

    
    class Meta:
            strict = True